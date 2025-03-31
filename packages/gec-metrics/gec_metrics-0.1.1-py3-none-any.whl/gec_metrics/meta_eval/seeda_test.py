from gec_metrics.metrics import MetricBaseForReferenceFree
from .seeda import MetaEvalSEEDA
import math

class Length(MetricBaseForReferenceFree):
    '''A pseudo-reference-free metric with character count as the score.
    '''
    def score_corpus(
        self,
        sources,
        hypotheses,
    ):
        return sum(len(h) for h in hypotheses)
    
    def score_sentence(
        self,
        sources,
        hypotheses,
    ):
        return [len(h) for h in hypotheses]
    
def test_corr_system():
    scorer = Length(Length.Config())
    meta_seeda = MetaEvalSEEDA(MetaEvalSEEDA.Config())
    out = meta_seeda.corr_system(scorer)
    
    corr_cls = MetaEvalSEEDA.Corr
    gold = MetaEvalSEEDA.SEEDASystemCorrOutput(
        ew_edit=corr_cls(pearson=0.42736690406501093, spearman=0.4545454545454546),
        ew_sent=corr_cls(pearson=0.4532076150049142, spearman=0.5454545454545455),
        ts_edit=corr_cls(pearson=0.4834645229702062, spearman=0.5944055944055945),
        ts_sent=corr_cls(pearson=0.4880423593992749, spearman=0.5524475524475525)
    )
    for k in gold.__dict__:
        assert math.isclose(gold.__dict__[k].pearson, out.__dict__[k].pearson, rel_tol=1e-6)
        assert math.isclose(gold.__dict__[k].spearman, out.__dict__[k].spearman, rel_tol=1e-6)

def test_corr_sentence():
    scorer = Length(Length.Config())
    meta_seeda = MetaEvalSEEDA(MetaEvalSEEDA.Config())
    out = meta_seeda.corr_sentence(scorer)
    
    corr_cls = MetaEvalSEEDA.Corr
    gold = MetaEvalSEEDA.SEEDASentenceCorrOutput(
        edit=corr_cls(accuracy=0.5365853658536586, kendall=0.07317073170731707),
        sent=corr_cls(accuracy=0.5455708346658139, kendall=0.09114166933162776)
    )
    for k in gold.__dict__:
        assert math.isclose(gold.__dict__[k].accuracy, out.__dict__[k].accuracy, rel_tol=1e-6)
        assert math.isclose(gold.__dict__[k].kendall, out.__dict__[k].kendall, rel_tol=1e-6)

def test_window_analysis():
    scorer = Length(Length.Config())
    meta_seeda = MetaEvalSEEDA(MetaEvalSEEDA.Config())
    out = meta_seeda.window_analysis_system(scorer, window=4)

    corr_cls = MetaEvalSEEDA.Corr
    gold = {
        (0, 3): corr_cls(pearson=-0.12719090478691203, spearman=0.19999999999999998),
        (1, 4): corr_cls(pearson=0.5900362463225375, spearman=0.7999999999999999),
        (2, 5): corr_cls(pearson=0.15518369973793955, spearman=0.39999999999999997),
        (3, 6): corr_cls(pearson=0.1205407475751627, spearman=0.39999999999999997),
        (4, 7): corr_cls(pearson=0.02436579076767783, spearman=0.0),
        (5, 8): corr_cls(pearson=-0.02121433684516863, spearman=0.19999999999999998),
        (6, 9): corr_cls(pearson=-0.16182645121353734, spearman=-0.39999999999999997),
        (7, 10): corr_cls(pearson=-0.23114390326454237, spearman=-0.39999999999999997),
        (8, 11): corr_cls(pearson=0.40786665626270313, spearman=0.39999999999999997)
    }
    out_ts_edit = out.ts_edit
    for k in out_ts_edit.keys():
        assert math.isclose(gold[k].pearson, out_ts_edit[k].pearson, rel_tol=1e-6)
        assert math.isclose(gold[k].spearman, out_ts_edit[k].spearman, rel_tol=1e-6)

    