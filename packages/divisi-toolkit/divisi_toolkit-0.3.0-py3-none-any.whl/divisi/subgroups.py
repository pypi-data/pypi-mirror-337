import scipy.sparse as sps
from scipy.sparse import csr_matrix, csc_matrix
import numpy as np
import pandas as pd
from .utils import pairwise_jaccard_similarities, detect_data_type, convert_to_native_types, powerset
from .discretization import DiscretizedData
import torch
import collections

class RuleFeatureBase:
    def __init__(self):
        self.empty = True
        self.num_univariate_features = 0
    
    def __hash__(self):
        return 0
    
    def __contains__(self, f):
        return False
    
    def __eq__(self, other):
        return type(other) is RuleFeatureBase
    
    def __lt__(self, other):
        return type(other) is not RuleFeatureBase
    
    def make_mask(self, inputs, univariate_masks=None, device='cpu'):
        return torch.ones(inputs.shape[0]).bool().to(device)

    def univariate_features(self):
        return tuple()
    
    def to_dict(self):
        return {"type": "base"}
    
    @staticmethod
    def from_dict(data):
        if data["type"] == "base":
            return RuleFeatureBase()
        elif data["type"] == "feature":
            return RuleFeature(data["col"], data["vals"])
        elif data["type"] == "negation":
            return RuleFeatureNegation(RuleFeatureBase.from_dict(data["feature"]))
        elif data["type"] == "and":
            return RuleFeatureAnd(RuleFeatureBase.from_dict(data["lhs"]), RuleFeatureBase.from_dict(data["rhs"]))
        elif data["type"] == "or":
            return RuleFeatureOr(RuleFeatureBase.from_dict(data["lhs"]), RuleFeatureBase.from_dict(data["rhs"]))
        raise ValueError(f"Unknown data type '{data['type']}'")
        
    def transform_features(self, transform_func):
        """
        Returns a new SliceFeatureBase instance with the given transform function
        applied to all SliceFeatures (not to the logical operations surrounding
        them).
        """
        return self
        
    def __str__(self):
        return "<empty>"
    
    def __repr__(self):
        return str(self)

class RuleFeature(RuleFeatureBase):
    def __init__(self, feature_name, allowed_values):
        super().__init__()
        self.empty = False
        self.feature_name = feature_name
        self.allowed_values = tuple(sorted(allowed_values))
        self.num_univariate_features = 1
        
    def __hash__(self):
        return hash((self.feature_name, self.allowed_values))
    
    def __str__(self):
        if len(self.allowed_values) != 1:
            return f"{self.feature_name} in ({', '.join(str(x) for x in self.allowed_values)})"
        return f"{self.feature_name} = {self.allowed_values[0]}"
    
    def __eq__(self, other):
        return isinstance(other, RuleFeature) and other.feature_name == self.feature_name and other.allowed_values == self.allowed_values
    
    def __lt__(self, other):
        if isinstance(other, RuleFeature):
            return self.feature_name < other.feature_name
        return True
    
    def __contains__(self, f):
        return self == f
    
    def univariate_features(self):
        return (self,)
    
    def to_dict(self):
        return {"type": "feature", "col": self.feature_name, "vals": self.allowed_values}

    def transform_features(self, transform_func):
        return transform_func(self)

    def make_mask(self, inputs, univariate_masks=None, device='cpu'):
        univ_mask = None
        # Check if univariate mask available in cache
        if univariate_masks is not None:
            univ_mask = univariate_masks.get(self, None)
            
        if univ_mask is None:
            if not self.allowed_values:
                univ_mask = torch.zeros(inputs.shape[0], dtype=torch.bool).to(device)
            else:
                for val in self.allowed_values:
                    if isinstance(inputs, (sps.csc_matrix, sps.csc_array, sps.csr_matrix, sps.csr_array)):
                        mask = torch.from_numpy((inputs[:,self.feature_name] == val).toarray().flatten()).to(device)
                    elif isinstance(inputs, np.ndarray):
                        mask = torch.from_numpy(inputs[:,self.feature_name] == val).to(device)
                    elif isinstance(inputs, torch.Tensor):
                        mask = inputs[:,self.feature_name] == val
                    else:
                        mask = inputs[self.feature_name] == val
                    if univ_mask is None:
                        univ_mask = mask.clone()
                    else:
                        univ_mask |= mask
                    
            # Update cache  
            if univariate_masks is not None and self not in univariate_masks:
                univariate_masks[self] = univ_mask

        return univ_mask
    
class RuleFeatureNegation(RuleFeatureBase):
    def __init__(self, feature):
        super().__init__()
        self.empty = False
        self.feature = feature
        self.num_univariate_features = self.feature.num_univariate_features
        
    def make_mask(self, inputs, univariate_masks=None, device='cpu'):
        return ~self.feature.make_mask(inputs, univariate_masks=univariate_masks, device='cpu')
    
    def univariate_features(self):
        return self.feature.univariate_features()

    def to_dict(self):
        return {"type": "negation", "feature": self.feature.to_dict()}
    
    def transform_features(self, transform_func):
        return RuleFeatureNegation(self.feature.transform_features(transform_func))

    def __hash__(self):
        return hash(self.feature)

    def __contains__(self, f):
        return self == f or self.feature == f

    def __eq__(self, other):
        return isinstance(other, RuleFeatureNegation) and other.feature == self.feature
    
    def __lt__(self, other):
        return self.feature < other
    
    def __str__(self):
        return f"~({str(self.feature)})"
    
class RuleFeatureAnd(RuleFeatureBase):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.empty = False
        self.lhs = lhs
        self.rhs = rhs
        self.num_univariate_features = self.lhs.num_univariate_features + self.rhs.num_univariate_features
        
    def make_mask(self, inputs, univariate_masks=None, device='cpu'):
        return (self.lhs.make_mask(inputs, univariate_masks=univariate_masks, device='cpu') & 
                self.rhs.make_mask(inputs, univariate_masks=univariate_masks, device='cpu'))

    def univariate_features(self):
        return (*self.lhs.univariate_features(), *self.rhs.univariate_features())

    def to_dict(self):
        return {"type": "and", "lhs": self.lhs.to_dict(), "rhs": self.rhs.to_dict()}

    def transform_features(self, transform_func):
        return RuleFeatureAnd(self.lhs.transform_features(transform_func),
                               self.rhs.transform_features(transform_func))

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def __contains__(self, f):
        return self == f or f in self.lhs or f in self.rhs

    def __eq__(self, other):
        return isinstance(other, RuleFeatureAnd) and other.lhs == self.lhs and other.rhs == self.rhs
    
    def __lt__(self, other):
        return self.lhs < other.lhs
    
    def __str__(self):
        return f"({str(self.lhs)} & {str(self.rhs)})"
        
class RuleFeatureOr(RuleFeatureBase):
    def __init__(self, lhs, rhs):
        super().__init__()
        self.empty = False
        self.lhs = lhs
        self.rhs = rhs
        self.num_univariate_features = self.lhs.num_univariate_features + self.rhs.num_univariate_features
        
    def make_mask(self, inputs, univariate_masks=None, device='cpu'):
        return (self.lhs.make_mask(inputs, univariate_masks=univariate_masks, device='cpu') |
                self.rhs.make_mask(inputs, univariate_masks=univariate_masks, device='cpu'))

    def univariate_features(self):
        return (*self.lhs.univariate_features(), *self.rhs.univariate_features())

    def to_dict(self):
        return {"type": "or", "lhs": self.lhs.to_dict(), "rhs": self.rhs.to_dict()}

    def transform_features(self, transform_func):
        return RuleFeatureOr(self.lhs.transform_features(transform_func),
                              self.rhs.transform_features(transform_func))

    def __hash__(self):
        return hash((self.lhs, self.rhs))

    def __contains__(self, f):
        return self == f or f in self.lhs or f in self.rhs

    def __eq__(self, other):
        return isinstance(other, RuleFeatureOr) and other.lhs == self.lhs and other.rhs == self.rhs
    
    def __lt__(self, other):
        return self.lhs < other.lhs
    
    def __str__(self):
        return f"({str(self.lhs)} | {str(self.rhs)})"

class Rule:
    def __init__(self, feature, score_values=None):
        """

        :param feature: a SliceFeatureBase instance describing the slice
        :param score_values: dictionary of score function to score values
        """
        assert isinstance(feature, RuleFeatureBase)
        self.feature = feature
        self.score_values = score_values or {}
        
    def to_dict(self):
        return {"feature": self.feature.to_dict(), "score_values": self.score_values}
    
    @staticmethod
    def from_dict(d):
        return Rule(RuleFeatureBase.from_dict(d["feature"]), score_values=d["score_values"])        
                
    def __hash__(self):
        return hash(self.feature)
    
    def __eq__(self, other):
        return isinstance(other, Rule) and other.feature == self.feature
    
    def __contains__(self, f):
        return f in self.feature
        
    def subslice(self, other_feature):
        """
        Creates a new Slice object with the given slice feature.
        """
        if self.feature.empty:
            return Rule(other_feature)
        return Rule(RuleFeatureAnd(self.feature, other_feature))
    
    def rescore(self, new_scores):
        """
        Returns a Rule object with identical feature values but a new dictionary
        of scores.
        """
        return Rule(self.feature, new_scores)

    def univariate_features(self):
        return self.feature.univariate_features()
    
    def make_mask(self, inputs, existing_mask=None, univariate_masks=None, device='cpu'):
        """
        Creates a binary mask representing membership in the given slice.
        
        :param inputs: a dataframe containing data points to check for membership
            in the slice
        :param existing_mask: if provided, a binary mask that will be intersected
            with the mask for the given slice
        :param univariate_masks: if provided, a dictionary mapping tuples of
            (col, val) to binary masks of the same length as inputs. This cache will
            be mutated if the function needs to compute a new univariate mask
            
        :return: a binary array where 1 indicates that a row is part of the
            slice
        """
        mask = existing_mask.clone() if existing_mask is not None else existing_mask
        
        if mask is None:
            mask = self.feature.make_mask(inputs, univariate_masks=univariate_masks, device=device)
        else:
            mask &= self.feature.make_mask(inputs, univariate_masks=univariate_masks, device=device)
        
        if mask is None:
            mask = torch.ones(inputs.shape[0]).bool().to(device)
        if isinstance(mask, pd.Series): mask = mask.values
        return mask

    def __str__(self):
        base = f"<Rule: "
        base += str(self.feature)
        if self.score_values:
            base += "; scores: "
            base += ", ".join(f"{score_name}: {value}" for score_name, value in self.score_values.items())
        base += ">"
        return base

    def __repr__(self):
        return str(self)
    
    def string_rep(self):
        return str(self.feature)

class IntersectionRule(Rule):
    """
    A special case of a Rule that consists of an AND'ed set of features, where
    each feature can be a SliceFeature or a SliceFeatureOr. Unlike normal Rule
    objects, IntersectionSlice instances are order-invariant when testing for
    equality and hashing.
    """
    def __init__(self, features, score_values=None, rule=None):
        if rule is not None:
            feature = rule
        else:
            if not features:
                feature = RuleFeatureBase()
            else:
                feature = features[-1]
                for i in range(len(features) - 2, -1, -1):
                    feature = RuleFeatureAnd(features[i], feature)
        super().__init__(feature, score_values=score_values)
        self.base_features = tuple(sorted(features))
        
    def __hash__(self):
        return hash(self.base_features)
    
    def __eq__(self, other):
        return isinstance(other, IntersectionRule) and other.base_features == self.base_features
    
    def subslice(self, other_feature):
        """
        Creates a new Rule object with the given slice feature.
        """
        if self.feature.empty:
            return IntersectionRule([other_feature])
        return IntersectionRule((*self.base_features, other_feature))

    def rescore(self, new_scores):
        """
        Returns a Rule object with identical feature values but a new dictionary
        of scores.
        """
        # make sure the order of the slice is preserved
        return IntersectionRule(self.base_features, new_scores, rule=self.feature)
    
    def sort_features(self, score_fn=None):
        """
        Sorts the features in the slice by the amount that they change the value
        returned by the given score function. The score function should take a
        Rule object and return a numerical value. The feature that causes the
        greatest decrease in the score function value relative to the overall
        slice will be placed first.
        """
        base_score = score_fn(self)
        ablated_slices = [(exclude_feature, IntersectionRule([f for f in self.base_features if f != exclude_feature]))
                          for exclude_feature in self.base_features]
        ablated_scores = [(*s, base_score - score_fn(s[1])) for s in ablated_slices]
        return IntersectionRule([x[0] for x in sorted(ablated_scores, key=lambda x: x[-1], reverse=True)],
                                 self.score_values)
        

def score_subgroups_batch(slices_to_score, inputs, ranking_fns, max_features, min_items_fraction=None, device='cpu', univariate_masks=None):
    univariate_masks = univariate_masks if univariate_masks is not None else {}
    scored_slices = {}
    
    for new_slice in slices_to_score:
        mask = new_slice.make_mask(inputs, univariate_masks=univariate_masks, device=device)
        if min_items_fraction is not None and mask.sum() / mask.shape[0] < min_items_fraction:
            scored_slices[new_slice] = None
            continue
        
        computed_scores = {}
        itemized_masks = [univariate_masks[f] for f in new_slice.univariate_features()]
        for key, scorer in ranking_fns.items():
            computed_scores[key] = scorer.calculate_score(new_slice, mask, itemized_masks).item()
        
        scored_slices[new_slice] = new_slice.rescore(computed_scores)
            
    return scored_slices

class RankedSubgroupList:
    """
    A type that manages a list of slices and associated scores. When the
    `RankedSubgroupList` is initialized, it contains results that are determined
    from a discovery set of points. When the `rank` method is called, the best
    slices are re-scored using an evaluation set of points (ideally held out
    from the discovery set), and ranked according to a given set of weights.
    This re-ranking process can be performed efficiently after the initial
    slice-finding operation.
    """
    
    def __init__(self, results, data, ranking_functions, eval_indexes=None, min_weight=0.0, max_weight=5.0, similarity_threshold=0.9, device='cpu', normalize_weights=True):
        """
        :param results: A list of Rule objects representing the results of a
            slice-finding operation
        :param data: The original discrete-valued dataframe or DiscretizedData
            used to compute scores
        :param ranking_functions: A dictionary of score names to score function
            objects
        :param similarity_threshold: Slices that have a higher Jaccard similarity
            than this threshold to already-returned slices will be omitted.
        """
        self.results = results
        self.data = data
        self.df = data.df if hasattr(data, 'df') else data
        self.eval_indexes = eval_indexes
        self.device = device
        if eval_indexes is not None:
            if isinstance(self.df, pd.DataFrame):
                self.eval_df = self.df.iloc[self.eval_indexes].values.astype(np.uint8)
            else:
                self.eval_df = self.df[self.eval_indexes]
                if isinstance(self.eval_df, csr_matrix):
                    self.eval_df = self.eval_df.tocsc()
            if not isinstance(self.eval_df, csc_matrix):
                self.eval_df = torch.from_numpy(self.eval_df).to(self.device)
            self.ranking_functions = {fn_name: fn.subslice(self.eval_indexes).to(self.device)
                                    for fn_name, fn in ranking_functions.items()}
            self.eval_mask = self.eval_indexes
        else:
            self.eval_df = self.df
            self.ranking_functions = ranking_functions
            self.eval_mask = np.arange(self.df.shape[0])
            
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.train_scores = pd.DataFrame([r.score_values for r in self.results])
        self.similarity_threshold = similarity_threshold
        self.normalize_weights = normalize_weights
        
        self.univariate_masks = {}
        self.score_cache = None # if the user sets this, we will cache eval scores

    def _rank_weighted_indexes(self, score_df, weights, k=None, normalize=True):
        """
        Computes the top indexes of a given score dataframe using the
        given dictionary of weights.
        """
        original_score_indexes = np.arange(len(score_df), dtype=np.uint32)
        weighted_score = np.zeros(len(score_df))
        for w_name, w in weights.items():
            weighted_score += w * (score_df[w_name] / (score_df[w_name].max() if normalize else 1))
        original_score_indexes = original_score_indexes[~np.isnan(weighted_score)]
        weighted_score = weighted_score[~np.isnan(weighted_score)]
        results = np.flip(np.argsort(weighted_score))
        if k is not None:
            results = results[:k]
        return original_score_indexes[results]
    
    def encode_rule(self, feature_set):
        """
        Returns a discretized version of the slice defined by the given dictionary
        representation of a slice feature.
        """
        try:
            return self.data.encode_rule(feature_set)
        except AttributeError:
            return Rule(feature_set)
        
    def score_slice(self, slice_obj, return_mask=False):
        if self.score_cache is not None and slice_obj in self.score_cache:
            group_scores, mask = self.score_cache[slice_obj]
        else:
            mask = slice_obj.make_mask(self.eval_df, univariate_masks=self.univariate_masks, device=self.device)
            itemized_masks = [self.univariate_masks[f] for f in slice_obj.univariate_features()]
            group_scores = {key: item.calculate_score(slice_obj, mask, itemized_masks).item()
                            for key, item in self.ranking_functions.items()}
            if self.score_cache is not None:
                self.score_cache[slice_obj] = (group_scores, mask)
            
        if return_mask:
            return group_scores, mask.cpu().numpy()
        return group_scores
        
    def rescore(self, result_indexes, return_masks=False):
        """
        Computes new evaluation-data scores for the results at the given indexes.
        
        :param result_indexes: An iterable of numerical index values to retrieve
            results from `self.results`.
        :param return_masks: If True, also return a sparse matrix of the masks
            used to compute scores on the eval data.
            
        :return: A tuple of (slices, scores) and optionally masks, where slices
            is a list of `Rule` objects, scores is a dataframe of eval scores
            according to each score function, and masks is a sparse csr_matrix
            of binary masks for each slice.
        """
        eval_scored_slices = []
        eval_scores = []
        if return_masks:
            mask_indptr = [0]
            mask_indices = []

        for result_idx in result_indexes:
            slice_obj = self.results[result_idx]
            group_scores, mask = self.score_slice(slice_obj, return_mask=True)
            
            eval_scores.append(group_scores)
            eval_scored_slices.append(slice_obj.rescore(group_scores))
            
            if return_masks:
                mask_indptr.append(mask_indptr[-1] + mask.sum())
                mask_indices.append(np.argwhere(mask).flatten())
            
        eval_scores = pd.DataFrame(eval_scores)
        
        result = (eval_scored_slices, eval_scores)
        if return_masks:
            mask_indices = np.concatenate(mask_indices)
            mask_mat = csr_matrix((np.ones(len(mask_indices), dtype=np.uint16),
                                mask_indices,
                                mask_indptr), dtype=np.uint16)
            return (*result, mask_mat)
        return result
        
    def rank(self, weights, num_to_rescore=100, n_slices=10, similarity_threshold=None, order_features=True, normalize_weights=None, decode=True):
        """
        Ranks and returns the top slices according to a given set of weights,
        filtering results that contain a very similar set of instances.
        
        :param weights: A dictionary mapping score function names to weight
            values. The weights must be within the `min_weight` and `max_weight` 
            used to calculate the original scores.
        :param num_to_rescore: The number of top-scoring slices from the
            discovery stage to re-score using the held-out evaluation data.
        :param n_slices: The number of slices to return.
        :param similarity_threshold: Slices that have a higher Jaccard similarity
            than this threshold to already-returned slices will be omitted.
        :param order_features: if True (default), sort the features in IntersectionSlices
            by their contribution to the slice's relevance.
        :param normalize_weights: If True (default), divide each score function's
            values by the max values they take to ensure that weights can be 
            adjusted in a user-friendly way.
        :param decode: If True and the results object was initialized as a
            DiscretizedData, convert returned subgroups to the original feature
            names. If False, subgroups will be returned in terms of column and 
            value indices.
        
        :return: A list of Rule objects with scores from the held-out
            evaluation data.
        """
        
        if not self.results:
            return []
        
        # Get the top num_to_rescore using the training scores
        top_train_indexes = self._rank_weighted_indexes(self.train_scores, weights, num_to_rescore)
        if not len(top_train_indexes):
            return []

        # Rescore these using evaluation data and rank
        eval_scored_slices, eval_scores, mask_mat = self.rescore(top_train_indexes, return_masks=True)
        top_eval_indexes = self._rank_weighted_indexes(eval_scores, weights, normalize=normalize_weights if normalize_weights is not None else self.normalize_weights)

        # Remove results with too-high jaccard similarity
        mask_similarities = pairwise_jaccard_similarities(mask_mat)
        ranked_result_idxs = []
        skip_idxs = set()
        for i in top_eval_indexes:
            if i in skip_idxs: continue
            ranked_result_idxs.append(i)
            sim_thresh = similarity_threshold if similarity_threshold is not None else self.similarity_threshold
            skip_idxs |= set(np.argwhere(mask_similarities[i] > sim_thresh).flatten().tolist())

        # Return top n_slices results
        ranked_results = [eval_scored_slices[i] for i in ranked_result_idxs]
        ranked_results = ranked_results[:min(len(ranked_results), n_slices)]
        def _score(slice_obj):
            scores = self.score_slice(slice_obj)
            return sum(scores.get(n, 0) * w for n, w in weights.items())
        ranked_results = [slice_obj.sort_features(_score) if isinstance(slice_obj, IntersectionRule) and order_features else slice_obj
                          for slice_obj in ranked_results]
        
        # Convert to original representation if requested
        if decode:
            try:
                ranked_results = [self.data.decode_rule(r) for r in ranked_results]
            except AttributeError:
                pass
        return ranked_results
    
    def slice_mask(self, slice_obj):
        """
        Calculates the slice mask for the given slice.
        """
        return slice_obj.make_mask(self.eval_df, univariate_masks=self.univariate_masks)
        
    def generate_slice_description(self, slice_obj, metrics=None, metrics_mask=None, return_slice_mask=False):
        """
        Creates JSON-serializable slice descriptions for a slice.
        
        :param slice: A Rule object
        :param metrics: If provided, a dictionary mapping metric names to
            series/arrays matching the shape of the original inputs. These metrics
            will be aggregated (histogram for continuous values, mean for
            binary values, value counts for categorical values)
        :param metrics_mask: If metrics is provided, this can be a mask over the
            inputs that determines over which input rows the metrics will be
            calculated
        :return: A dictionary containing metadata and user-readable
            descriptions for the slice.
        """            
        slice_desc = {
            "scoreValues": slice_obj.score_values, 
            "rawFeature": slice_obj.feature.to_dict(),
            "stringRep": slice_obj.string_rep()
        }
        try:
            slice_desc["feature"] = self.data.decode_rule(slice_obj).feature.to_dict()
        except AttributeError:
            slice_desc["feature"] = slice_obj.feature.to_dict()
            
        slice_metrics = {}
        if self.score_cache is not None and slice_obj in self.score_cache:
            slice_mask = self.score_cache[slice_obj][1]
        else:
            slice_mask = slice_obj.make_mask(self.eval_df, univariate_masks=self.univariate_masks, device=self.device).cpu().numpy()
        if metrics_mask is not None:
            slice_mask &= metrics_mask
        mask = np.arange(self.df.shape[0])[self.eval_mask][slice_mask]
        base_mask = self.eval_mask
        if metrics_mask is not None:
            base_mask = base_mask[metrics_mask]
            eval_count = self.eval_df[metrics_mask].shape[0]
        else:
            eval_count = self.eval_df.shape[0]
        
        slice_metrics["Count"] = {"type": "count", "count": len(mask), "share": len(mask) / eval_count}
        slice_desc["isEmpty"] = len(mask) == 0
        if metrics:
            for metric_name, data in metrics.items():
                if isinstance(data, dict):
                    # User-specified options
                    options = data
                    data = options["data"]
                else:
                    options = {}
                data_type = options.get("type", detect_data_type(data))
                if data_type == "binary":
                    slice_metrics[metric_name] = {"type": data_type, 
                                                  "count": np.nansum(data[mask]),
                                                  "mean": np.nanmean(data[mask]), 
                                                  "share": np.nansum(data[mask]) / np.nansum(data[base_mask])}
                elif data_type == "categorical":
                    if np.issubdtype(data.dtype, np.number):
                        counts = dict(zip(*np.unique(data[mask], return_counts=True)))
                    else:
                        counts = {v: count for v, count in collections.Counter(data[mask]).items() if v not in {None, np.nan, pd.NA}}
                    slice_metrics[metric_name] = {"type": data_type, 
                                                  "counts": counts}
                else:
                    if "bins" in options:
                        hist_bins = options["bins"]
                    else:
                        # Calculate the range of the data and choose an appropriate
                        # scale for the bin size
                        min_val = np.nanmin(data)
                        max_val = np.nanmax(data)
                        data_range = max_val - min_val
                        bin_scale = np.floor(np.log10(data_range))
                        if data_range / (10 ** bin_scale) < 2.5:
                            bin_scale -= 1 # Make sure there aren't only 2-3 bins
                        upper_tol = 2 if (np.ceil(max_val / (10 ** bin_scale))) * (10 ** bin_scale) == max_val else 1
                        hist_bins = np.arange(np.floor(min_val / (10 ** bin_scale)) * (10 ** bin_scale),
                                              (np.ceil(max_val / (10 ** bin_scale)) + upper_tol) * (10 ** bin_scale),
                                              10 ** bin_scale)
                    hist_values, _ = np.histogram(data[mask], bins=hist_bins)
                    slice_metrics[metric_name] = {"type": data_type,
                                                  "hist": dict(zip(hist_bins, hist_values)),
                                                  "mean": np.nanmean(data[mask])}
        slice_desc["metrics"] = slice_metrics
            
        result = convert_to_native_types(slice_desc)
        if return_slice_mask:
            return result, mask
        return result
