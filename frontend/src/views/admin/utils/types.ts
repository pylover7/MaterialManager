export interface FormItemProps {
  key: number;
  content: string;
  id?: string;
  created_at?: string;
  updated_at?: string;
}

export interface FormProps {
  formData: [FormItemProps];
}

export type SelectOptList = Array<{
  label: string;
  value: string | boolean | number;
}>;

export interface SelectOpt {
  label: string;
  value: string | boolean | number;
}
