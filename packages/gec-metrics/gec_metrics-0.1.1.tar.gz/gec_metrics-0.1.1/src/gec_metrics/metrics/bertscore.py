from .base import MetricBaseForSourceFree
from dataclasses import dataclass
from bert_score import BERTScorer
import os
import torch

class BertScore(MetricBaseForSourceFree):
    @dataclass
    class Config(MetricBaseForSourceFree.Config):
        '''BERTScore configuration.
        
        - model_type (str): Embedding model.
        - num_layers (int): The layer of representation to use.
            If None, the pre-difined one is used. (See bert_score.utils.model2layers.)
        - nthreads (int): Number of threads.
        - idf (bool): Whether to use idf or not.
        - idf_sents (list[str]): Sentences to compute idf weights.
        - rescale_with_baselines (bool): Whether to rescale scores.
        - baseline_path (str): Path to .tsv file.
            If None, the pre-defined one is used. (See bert_score.rescale_baseline.*.tsv)
        - use_fast_tokenizer (bool): Whether to use fast tokenizer.
        - score_type (str): "p" (precision) or "r" (recall) or "f" (F1) score.
        '''
        model_type: str = 'bert-base-uncased'
        num_layers: int = None
        batch_size: int = 64
        nthreads: int = 4
        all_layers: bool = False
        idf: bool = False
        idf_sents: list[str] = None
        lang: str = 'en'
        rescale_with_baseline: bool = True
        baseline_path: str = None
        use_fast_tokenizer: bool = False
        score_type: str = 'f'

    def __init__(self, config: Config = None):
        super().__init__(config)
        assert self.config.score_type in ['p', 'r', 'f']
        self.scorer = BERTScorer(
            model_type=self.config.model_type,
            num_layers=self.config.num_layers,
            batch_size=self.config.batch_size,
            nthreads=self.config.nthreads,
            all_layers=self.config.all_layers,
            idf=self.config.idf,
            idf_sents=self.config.idf_sents,
            lang=self.config.lang,
            rescale_with_baseline=self.config.rescale_with_baseline,
            baseline_path=self.config.baseline_path,
            use_fast_tokenizer=self.config.use_fast_tokenizer
        )
        self.scorer._model.eval()
        if torch.cuda.is_available():
            self.scorer._model.cuda()
        
    def score_sentence(
        self,
        hypotheses: list[str],
        references: list[list[str]]
    ) -> list[float]:
        '''Calculate sentence-level scores.

        Args:
            hypotheses (list[str]): Corrected sentences.
                The shape is (num_sentences, )
            references (list[list[str]]): Reference sentences.
                The shape is (num_references, num_sentences).
        
        Returns:
            list[float]: The sentence-level scores.
        '''
        # (num_refs, num_sents) -> (num_sents, num_refs)
        references = list(zip(*references))
        output = self.scorer.score(
            cands=hypotheses,
            refs=references
        )
        idx = {
            'p': 0,
            'r': 1,
            'f': 2
        }[self.config.score_type]
        scores = output[idx].view(-1).tolist()
        return scores