export interface ITask {
  SubTaskID: number;
  SubTaskNumber: string;
  SubjectID: number;
  SubjectName: string;
  EnglishName: string;
  TaskID: number;
  TaskTitle: string;
  VariantID: null | number;
  VariantName: null | string;
  TypeVariant: null | string;
  YearVariant: null | number;
  NumberVariant: null | number;
  DifficultyLevel: null | number;
  Description: null | string;
  Blocks: [] | IBlock[];
  Comment: null | string;
  Creator: string;
  CreatedDate: string;
  Editor: null | string;
  EditedDate: null | string;
  Files: [] | string[];
  CompletionStatus: null | string;
  Score: null | number;
}

export interface IData {
  Blocks: IBlock[];
  Comment: string | null;
  Creator: string;
  Description: string;
  DifficultyLevel: number | null;
  Files: [];
  NumberVarinat: number | null;
  SubTaskID: number;
  SubTaskNumber: number;
  SubjectID: number;
  SubjectName: string;
  TaskID: number;
  TaskTitle: string;
  TypeVariant: string | null;
  UploadDate: string;
  VariantID: number;
  VariantName: string;
  YearVariant: number | null;
  CompletionStatus: string | null;
}

export interface IBlock {
  type: string;
  content: string;
}
