use std::collections::HashMap;
use std::error::Error;

pub enum ModelBiasMetrics {
    DifferenceInPositivePredictedLabels,
    DisparateImpact,
    AccuracyDifference,
    RecallDifference,
    DifferenceInConditionalAcceptance,
    DifferenceInAcceptanceRate,
    SpecialityDifference,
    DifferenceInConditionalRejection,
    DifferenceInRejectionRate,
    TreatmentEquity,
    ConditionalDemographicDesparityPredictedLabels,
    GeneralizedEntropy,
}

pub const FULL_MODEL_BIAS_METRICS: [ModelBiasMetrics; 12] = [
    ModelBiasMetrics::DifferenceInPositivePredictedLabels,
    ModelBiasMetrics::DisparateImpact,
    ModelBiasMetrics::AccuracyDifference,
    ModelBiasMetrics::RecallDifference,
    ModelBiasMetrics::DifferenceInConditionalAcceptance,
    ModelBiasMetrics::DifferenceInAcceptanceRate,
    ModelBiasMetrics::SpecialityDifference,
    ModelBiasMetrics::DifferenceInConditionalRejection,
    ModelBiasMetrics::DifferenceInRejectionRate,
    ModelBiasMetrics::TreatmentEquity,
    ModelBiasMetrics::ConditionalDemographicDesparityPredictedLabels,
    ModelBiasMetrics::GeneralizedEntropy,
];

pub fn map_string_to_metrics(
    metrics: Vec<String>,
) -> Result<Vec<ModelBiasMetrics>, Box<dyn Error>> {
    let mut tms: Vec<ModelBiasMetrics> = Vec::with_capacity(metrics.len());
    for str_m in metrics.into_iter() {
        let m = ModelBiasMetrics::try_from(str_m.as_str())?;
        tms.push(m)
    }
    Ok(tms)
}

impl TryFrom<&str> for ModelBiasMetrics {
    type Error = String;
    fn try_from(value: &str) -> Result<Self, Self::Error> {
        match value {
            "DifferenceInPositivePredictedLabels" => Ok(Self::DifferenceInPositivePredictedLabels),
            "DisparateImpact" => Ok(Self::DisparateImpact),
            "AccuracyDifference" => Ok(Self::AccuracyDifference),
            "RecallDifference" => Ok(Self::RecallDifference),
            "DifferenceInConditionalAcceptance" => Ok(Self::DifferenceInConditionalAcceptance),
            "DifferenceInAcceptanceRate" => Ok(Self::DifferenceInAcceptanceRate),
            "SpecialityDifference" => Ok(Self::SpecialityDifference),
            "DifferenceInConditionalRejection" => Ok(Self::DifferenceInConditionalRejection),
            "DifferenceInRejectionRate" => Ok(Self::DifferenceInRejectionRate),
            "TreatmentEquity" => Ok(Self::TreatmentEquity),
            "ConditionalDemographicDesparityPredictedLabels" => {
                Ok(Self::ConditionalDemographicDesparityPredictedLabels)
            }
            "GeneralizedEntropy" => Ok(Self::GeneralizedEntropy),
            _ => Err("Invalid metric passed".into()),
        }
    }
}

pub struct PostTrainingData {
    pub facet_a_scores: Vec<i16>,
    pub facet_d_scores: Vec<i16>,
    pub facet_a_trues: Vec<i16>,
    pub facet_d_trues: Vec<i16>,
}

pub struct PostTrainingComputations {
    pub true_positives_a: f32,
    pub true_positives_d: f32,
    pub false_positives_a: f32,
    pub false_positives_d: f32,
    pub false_negatives_a: f32,
    pub false_negatives_d: f32,
    pub true_negatives_a: f32,
    pub true_negatives_d: f32,
}

impl PostTrainingData {
    pub fn general_data_computations(&self) -> PostTrainingComputations {
        PostTrainingComputations {
            true_positives_a: self.true_positives_a(),
            true_positives_d: self.true_positives_d(),
            false_positives_a: self.false_positives_a(),
            false_positives_d: self.false_positives_d(),
            false_negatives_a: self.false_negatives_a(),
            false_negatives_d: self.false_negatives_d(),
            true_negatives_a: self.true_negatives_a(),
            true_negatives_d: self.true_negatives_d(),
        }
    }

    fn true_positives_a(&self) -> f32 {
        self.facet_a_scores
            .iter()
            .zip(self.facet_a_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 1_i16 && *y_true == 1_i16 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
            .into()
    }

    fn true_positives_d(&self) -> f32 {
        self.facet_d_scores
            .iter()
            .zip(self.facet_d_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 1_i16 && *y_true == 1_i16 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn false_positives_a(&self) -> f32 {
        self.facet_a_scores
            .iter()
            .zip(self.facet_a_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 1_i16 && *y_true == 0_i16 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn false_positives_d(&self) -> f32 {
        self.facet_d_scores
            .iter()
            .zip(self.facet_d_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 1 && *y_true == 0 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn false_negatives_a(&self) -> f32 {
        self.facet_a_scores
            .iter()
            .zip(self.facet_a_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 0 && *y_true == 1 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn false_negatives_d(&self) -> f32 {
        self.facet_d_scores
            .iter()
            .zip(self.facet_d_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 0 && *y_true == 1 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn true_negatives_a(&self) -> f32 {
        self.facet_a_scores
            .iter()
            .zip(self.facet_a_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 0 && *y_true == 0 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }

    fn true_negatives_d(&self) -> f32 {
        self.facet_d_scores
            .iter()
            .zip(self.facet_d_trues.iter())
            .map(|(y_pred, y_true)| {
                if *y_pred == 0 && *y_true == 0 {
                    1_f32
                } else {
                    0_f32
                }
            })
            .sum::<f32>()
    }
}

pub fn diff_in_pos_proportion_in_pred_labels(data: &PostTrainingData) -> f32 {
    let q_prime_a: f32 = data.facet_a_scores.iter().sum::<i16>() as f32
        / data.facet_a_trues.iter().sum::<i16>() as f32;
    let q_prime_d: f32 = data.facet_d_scores.iter().sum::<i16>() as f32
        / data.facet_d_trues.iter().sum::<i16>() as f32;

    return q_prime_a - q_prime_d;
}

pub fn disparate_impact(data: &PostTrainingData) -> f32 {
    let q_prime_a: f32 = data.facet_a_scores.iter().sum::<i16>() as f32
        / data.facet_d_trues.iter().sum::<i16>() as f32;
    let q_prime_d: f32 = data.facet_d_scores.iter().sum::<i16>() as f32
        / data.facet_d_trues.iter().sum::<i16>() as f32;

    if q_prime_d == 0.0 {
        return 0.0;
    }
    q_prime_a / q_prime_d
}

pub fn accuracy_difference(
    pre_computed_data: &PostTrainingComputations,
    data: &PostTrainingData,
) -> f32 {
    let acc_a: f32 = (pre_computed_data.true_positives_a + pre_computed_data.true_negatives_a)
        / data.facet_a_scores.len() as f32;

    let acc_d: f32 = (pre_computed_data.true_positives_d + pre_computed_data.true_negatives_d)
        / data.facet_d_scores.len() as f32;

    return acc_a - acc_d;
}

pub fn recall_difference(pre_computed_data: &PostTrainingComputations) -> f32 {
    let recall_a: f32 = pre_computed_data.true_positives_a
        / (pre_computed_data.true_positives_a + pre_computed_data.false_negatives_a);
    let recall_d: f32 = pre_computed_data.true_positives_d
        / (pre_computed_data.true_positives_d + pre_computed_data.false_negatives_d);

    recall_a - recall_d
}

pub fn diff_in_cond_acceptance(data: &PostTrainingData) -> f32 {
    let sum_true_facet_a: f32 = data.facet_a_trues.iter().sum::<i16>().into();
    let sum_scores_facet_a: f32 = data.facet_a_scores.iter().sum::<i16>().into();
    let c_facet_a: f32 = sum_true_facet_a / sum_scores_facet_a;

    let sum_true_facet_d: f32 = data.facet_d_trues.iter().sum::<i16>().into();
    let sum_scores_facet_d: f32 = data.facet_d_scores.iter().sum::<i16>().into();
    let c_facet_d: f32 = sum_true_facet_d / sum_scores_facet_d;

    c_facet_a - c_facet_d
}

pub fn diff_in_acceptance_rate(pre_computed_data: &PostTrainingComputations) -> f32 {
    let precision_a: f32 = pre_computed_data.true_positives_a
        / (pre_computed_data.true_positives_a + pre_computed_data.false_positives_a);
    let precision_d: f32 = pre_computed_data.true_positives_d
        / (pre_computed_data.true_positives_d + pre_computed_data.false_positives_d);

    precision_a - precision_d
}

pub fn specailty_difference(pre_computed_data: &PostTrainingComputations) -> f32 {
    let true_negative_rate_d: f32 = pre_computed_data.true_negatives_d
        / (pre_computed_data.true_negatives_d + pre_computed_data.false_positives_d);
    let true_negative_rate_a: f32 = pre_computed_data.true_negatives_a
        / (pre_computed_data.true_negatives_a + pre_computed_data.false_positives_a);

    true_negative_rate_d - true_negative_rate_a
}

pub fn diff_in_cond_rejection(data: &PostTrainingData) -> f32 {
    let n_prime_d: f32 = data
        .facet_d_scores
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>();
    let n_d: f32 = data
        .facet_d_trues
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>();
    let r_d: f32 = n_d / n_prime_d;

    let n_prime_a: f32 = data
        .facet_a_scores
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>();
    let n_a: f32 = data
        .facet_a_trues
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>();
    let r_a: f32 = n_a / n_prime_a;

    r_d - r_a
}

pub fn diff_in_rejection_rate(pre_computed_data: &PostTrainingComputations) -> f32 {
    let value_d: f32 = pre_computed_data.true_negatives_d
        / (pre_computed_data.true_negatives_d + pre_computed_data.false_negatives_d);
    let value_a: f32 = pre_computed_data.true_negatives_a
        / (pre_computed_data.true_negatives_a + pre_computed_data.false_negatives_a);

    value_d - value_a
}

pub fn treatment_equity(pre_computed_data: &PostTrainingComputations) -> f32 {
    let value_d: f32 = pre_computed_data.false_negatives_d / pre_computed_data.false_positives_d;
    let value_a: f32 = pre_computed_data.false_negatives_a / pre_computed_data.false_positives_a;

    value_d - value_a
}

pub fn cond_dem_desp_in_pred_labels(data: &PostTrainingData) -> f32 {
    let n_prime_0: f32 = data
        .facet_a_scores
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>()
        + data
            .facet_d_scores
            .iter()
            .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
            .sum::<f32>();

    let n_prime_1: f32 = data
        .facet_a_scores
        .iter()
        .map(|value| if *value == 1 { 1_f32 } else { 0_f32 })
        .sum::<f32>()
        + data
            .facet_d_scores
            .iter()
            .map(|value| if *value == 1 { 1_f32 } else { 0_f32 })
            .sum::<f32>();

    let n_prime_d_0: f32 = data
        .facet_d_scores
        .iter()
        .map(|value| if *value == 0 { 1_f32 } else { 0_f32 })
        .sum::<f32>();
    let n_prime_d_1: f32 = data
        .facet_d_scores
        .iter()
        .map(|value| if *value == 1 { 1_f32 } else { 0_f32 })
        .sum::<f32>();

    n_prime_d_0 / n_prime_0 - n_prime_d_1 / n_prime_1
}

pub fn generalized_entropy(data: &PostTrainingData) -> f32 {
    let y_true = [data.facet_a_trues.clone(), data.facet_d_trues.clone()].concat();
    let y_pred = [data.facet_a_scores.clone(), data.facet_d_scores.clone()].concat();

    let benefits: Vec<f32> = y_true
        .iter()
        .zip(y_pred.iter())
        .map(|(y_true, y_pred)| {
            if *y_pred == 0 && *y_true == 1 {
                0_f32
            } else if *y_pred == 1 && *y_true == 1 {
                1_f32
            } else {
                2_f32
            }
        })
        .collect();

    let sum: f32 = benefits.iter().sum::<f32>();
    let n = benefits.len() as f32;
    let mean: f32 = sum / n;
    let transformed_benefits: Vec<f32> = benefits
        .iter()
        .map(|value| ((*value / mean).powf(2.0)) - 1.0)
        .collect();
    let result: f32 = transformed_benefits.iter().sum::<f32>();
    result * (0.5 * n)
}

pub fn post_training_bias(data: PostTrainingData) -> Result<HashMap<String, f32>, String> {
    let pre_computed_data: PostTrainingComputations = data.general_data_computations();
    let mut result: HashMap<String, f32> = HashMap::with_capacity(12);
    result.insert(
        "DifferenceInPositivePredictedLabels".into(),
        diff_in_pos_proportion_in_pred_labels(&data),
    );
    result.insert("DisparateImpact".into(), disparate_impact(&data));
    result.insert(
        "AccuracyDifference".into(),
        accuracy_difference(&pre_computed_data, &data),
    );
    result.insert(
        "RecallDifference".into(),
        recall_difference(&pre_computed_data),
    );
    result.insert(
        "DifferenceInConditionalAcceptance".into(),
        diff_in_cond_acceptance(&data),
    );
    result.insert(
        "DifferenceInAcceptanceRate".into(),
        diff_in_acceptance_rate(&pre_computed_data),
    );
    result.insert(
        "SpecialityDifference".into(),
        specailty_difference(&pre_computed_data),
    );
    result.insert(
        "DifferenceInConditionalRejection".into(),
        diff_in_cond_rejection(&data),
    );
    result.insert(
        "DifferenceInRejectionRate".into(),
        diff_in_rejection_rate(&pre_computed_data),
    );
    result.insert(
        "TreatmentEquity".into(),
        treatment_equity(&pre_computed_data),
    );
    result.insert(
        "ConditionalDemographicDesparityPredictedLabels".into(),
        cond_dem_desp_in_pred_labels(&data),
    );
    result.insert("GeneralizedEntropy".into(), generalized_entropy(&data));

    Ok(result)
}
