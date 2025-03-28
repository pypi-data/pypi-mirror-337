import json
import logging
import os
import pickle
from collections import namedtuple

import torch

from synthtexteval.eval.downstream.coref.consts import SPEAKER_START, SPEAKER_END, NULL_ID_FOR_COREF
from synthtexteval.eval.downstream.coref.utils import flatten_list_of_lists
from torch.utils.data import Dataset

CorefExample = namedtuple("CorefExample", ["token_ids", "clusters"])

logger = logging.getLogger(__name__)


class CorefDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_seq_length=-1):
        self.tokenizer = tokenizer
        examples, self.max_mention_num, self.max_cluster_size, self.max_num_clusters = self._parse_jsonlines(file_path)
        self.max_seq_length = max_seq_length
        self.pretokenized_examples = examples
        self.examples, self.lengths, self.num_examples_filtered = self._tokenize(examples)
        
    def _parse_jsonlines(self, file_path):
        examples = []
        max_mention_num = -1
        max_cluster_size = -1
        max_num_clusters = -1
        num_examples = 0
        with open(file_path, 'r') as f:
            for line in f:
                num_examples += 1
                d = json.loads(line.strip())
                doc_key = d["doc_key"]
                input_words = flatten_list_of_lists(d["sentences"])
                clusters = d["clusters"]
                max_mention_num = max(max_mention_num, len(flatten_list_of_lists(clusters)))
                max_cluster_size = max(max_cluster_size, max(len(cluster) for cluster in clusters) if clusters else 0)
                max_num_clusters = max(max_num_clusters, len(clusters) if clusters else 0)
                speakers = flatten_list_of_lists(d["speakers"])
                examples.append((doc_key, input_words, clusters, speakers))
                # if num_examples == 10:
                #     break
        return examples, max_mention_num, max_cluster_size, max_num_clusters

    def _tokenize(self, examples):
        coref_examples = []
        lengths = []
        num_examples_filtered = 0
        for doc_key, words, clusters, speakers in examples:
            word_idx_to_start_token_idx = dict()
            word_idx_to_end_token_idx = dict()
            end_token_idx_to_word_idx = [0]  # for <s>

            token_ids = []
            last_speaker = None
            # print('doc key', doc_key, len(words))
            for idx, word in enumerate(words):
                # if last_speaker != speaker:
                #     speaker_prefix = [SPEAKER_START] + self.tokenizer.encode(" " + speaker,
                #                                                              add_special_tokens=False) + [SPEAKER_END]
                #     last_speaker = speaker
                # else:
                    # speaker_prefix = []
                speaker_prefix = []
                for _ in range(len(speaker_prefix)):
                    end_token_idx_to_word_idx.append(idx)
                token_ids.extend(speaker_prefix)
                word_idx_to_start_token_idx[idx] = len(token_ids) + 1  # +1 for <s>
                tokenized = self.tokenizer.encode(" " + word, add_special_tokens=False)
                for _ in range(len(tokenized)):
                    end_token_idx_to_word_idx.append(idx)
                token_ids.extend(tokenized)
                word_idx_to_end_token_idx[idx] = len(token_ids)  # old_seq_len + 1 (for <s>) + len(tokenized_word) - 1 (we start counting from zero) = len(token_ids)

            if 0 < self.max_seq_length < len(token_ids):
                num_examples_filtered += 1
                continue
            # print('[word_idx_to_start_token_idx]', word_idx_to_start_token_idx)
            # print('[clusters]', clusters)
            # print('len words', len(words))
            # print()
            # print()
            new_clusters = [
                [(word_idx_to_start_token_idx[start], word_idx_to_end_token_idx[end]) for start, end in cluster] for
                cluster in clusters]
            lengths.append(len(token_ids))

            coref_examples.append(((doc_key, end_token_idx_to_word_idx), CorefExample(token_ids=token_ids, clusters=new_clusters)))
        return coref_examples, lengths, num_examples_filtered

    def _reverse_tokenize_clusters(self, examples, token_clusters):
        coref_examples = []
        lengths = []
        num_examples_filtered = 0
        word_clusters = {}
        for doc_key, words, clusters, speakers in examples:
            word_idx_to_start_token_idx = dict()
            word_idx_to_end_token_idx = dict()
            token_idx_to_word_idx = dict()
            end_token_idx_to_word_idx = [0]  # for <s>

            token_ids = []
            last_speaker = None
            for idx, word in enumerate(words):
               
                speaker_prefix = []
                for _ in range(len(speaker_prefix)):
                    end_token_idx_to_word_idx.append(idx)
                token_ids.extend(speaker_prefix)
                word_idx_to_start_token_idx[idx] = len(token_ids) + 1  # +1 for <s>
                token_idx_to_word_idx[len(token_ids) + 1] = idx
                tokenized = self.tokenizer.encode(" " + word, add_special_tokens=False)
                for _ in range(len(tokenized)):
                    end_token_idx_to_word_idx.append(idx)
                token_ids.extend(tokenized)
                word_idx_to_end_token_idx[idx] = len(token_ids)  # old_seq_len + 1 (for <s>) + len(tokenized_word) - 1 (we start counting from zero) = len(token_ids)
                token_idx_to_word_idx[len(token_ids)] = idx
            if 0 < self.max_seq_length < len(token_ids):
                num_examples_filtered += 1
                continue
            token_clusters_ = token_clusters[doc_key]
            max_token_idx = max(list(token_idx_to_word_idx.keys()))
            curr_word_idx = 0
            for i in range(max_token_idx+2):
                if i in token_idx_to_word_idx:
                    curr_word_idx = token_idx_to_word_idx[i]
                else:
                    token_idx_to_word_idx[i] = curr_word_idx

            # print('[max_token_idx]', max_token_idx)    
            # print('[word_idx_to_start_token_idx]', word_idx_to_start_token_idx)
            # print('[word_idx_to_end_token_idx]', word_idx_to_end_token_idx)
            # print('[token_idx_to_word_idx]', token_idx_to_word_idx)
            # print('[token_clusters_]', token_clusters_)
            word_clusters_ = [
                    [(token_idx_to_word_idx[start], token_idx_to_word_idx[end]) for start, end in cluster] for
                    cluster in token_clusters_
            ]
            word_clusters[doc_key] = word_clusters_

        return word_clusters
    
    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        return self.examples[item]

    def pad_clusters_inside(self, clusters):
        return [cluster + [(NULL_ID_FOR_COREF, NULL_ID_FOR_COREF)] * (self.max_cluster_size - len(cluster)) for cluster
                in clusters]

    def pad_clusters_outside(self, clusters):
        return clusters + [[]] * (self.max_num_clusters - len(clusters))

    def pad_clusters(self, clusters):
        clusters = self.pad_clusters_outside(clusters)
        clusters = self.pad_clusters_inside(clusters)
        return clusters

    def pad_batch(self, batch, max_length):
        max_length += 2  # we have additional two special tokens <s>, </s>
        padded_batch = []
        for example in batch:
            # breakpoint()
            encoded_dict = self.tokenizer.encode_plus(example[0],
                                                      add_special_tokens=True,
                                                      truncation=True,
                                                      padding='max_length', #   pad_to_max_length=True,
                                                      max_length=max_length,
                                                      return_attention_mask=True,
                                                      return_tensors='pt')
            # print('max_length', max_length)
            # exit(0)
            clusters = self.pad_clusters(example.clusters)
            example = (encoded_dict["input_ids"], encoded_dict["attention_mask"]) + (torch.tensor(clusters),)
            padded_batch.append(example)
        tensored_batch = tuple(torch.stack([example[i].squeeze() for example in padded_batch], dim=0) for i in range(len(example)))
        return tensored_batch




def get_dataset(args, tokenizer, file_path):
    coref_dataset = CorefDataset(file_path, tokenizer, max_seq_length=args.max_seq_length)
    return coref_dataset

# def get_dataset(args, tokenizer, silver=False):
#     read_from_cache, file_path = False, ''
#     if silver and os.path.exists(args.predict_file_cache):
#         file_path = args.predict_file_cache
#         read_from_cache = True
#     elif (not silver) and os.path.exists(args.test_file_cache):
#         file_path = args.test_file_cache
#         read_from_cache = True
#     logger.info(f'[CorefDataset][get_dataset] args.max_seq_length {args.max_seq_length}')

#     if read_from_cache:
#         logger.info(f"[READ FROM CACHE ] Reading dataset from {file_path}")

#         with open(file_path, 'rb') as f:
#             return pickle.load(f)

#     file_path, cache_path = (args.predict_file, args.predict_file_cache) if silver else (args.test_file, args.test_file_cache)
#     # exit(0)
#     coref_dataset = CorefDataset(file_path, tokenizer, max_seq_length=args.max_seq_length)
#     with open(cache_path, 'wb') as f:
#         pickle.dump(coref_dataset, f)

#     return coref_dataset
