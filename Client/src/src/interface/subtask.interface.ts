export interface ITask {
  StudentTaskID: number;
  StudentID: number;
  SubTaskID: number;
  CompletionStatus: string;
  DeadlineDate: string;
  Attempts: number;
  Login: string;
  ID: number;
  Name: string;
  TaskID: number;
  TaskTitle: string;
  SubTaskNumber: number;
  ImagePath: string;
  Description: string;
  VariantID: number;
  VariantName: string;
  Score: number;
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
}


export interface IBlock {
  type: string;
  content: string;
}
