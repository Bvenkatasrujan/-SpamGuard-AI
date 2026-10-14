export type LabelType = 'spam' | 'ham' | 'uncertain';
export type RiskLevel = 'high' | 'medium' | 'low' | 'uncertain';

export interface TextMetadata {
  message_length: number;
  word_count: number;
  character_count: number;
  digit_count: number;
  digit_ratio: number;
  uppercase_count: number;
  uppercase_ratio: number;
  special_character_count: number;
  punctuation_count: number;
  exclamation_count: number;
  question_mark_count: number;
  currency_symbol_count: number;
  emoji_count: number;
  url_count: number;
  phone_number_count: number;
  email_count: number;
  has_url: boolean;
  has_shortened_url: boolean;
  is_email?: boolean;
  has_subject_header?: boolean;
  line_count?: number;
}

export interface PredictionResult {
  label: LabelType;
  is_spam: boolean | null;
  confidence: number;
  risk_level: RiskLevel;
  indicators: string[];
  metadata: TextMetadata;
}

export interface HistoryItem extends PredictionResult {
  id: string;
  timestamp: string;
  message: string;
}

export interface ModelMetadata {
  model_name: string;
  algorithm: string;
  feature_configuration: string;
  dataset: string;
  version: string;
  training_date: string;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    roc_auc: number;
    pr_auc: number;
    false_positives: number;
    false_negatives: number;
    true_positives: number;
    true_negatives: number;
  };
}
