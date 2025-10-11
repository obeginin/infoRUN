export interface ITask {
<<<<<<< Updated upstream
  Attempts: number;
  Blocks: IBlock[] | [];
  Comment: null | string;
  CompletionDate: null | string;
  CompletionStatus: null | string;
  DeadlineDate: null | string;
  Description: null | string;
  DifficultyLevel: null | number;
  ID: null | number;
  Login: string;
  ModifiedDate: null | string;
  Name: null | string;
  NumberVarinat: null | number;
  Score: null | number;
  SolutionStudentPath: null | string;
  StartDate: null | string;
  StudentAnswer: null | string;
  StudentID: number;
  StudentTaskID: number;
  SubTaskID: number;
  SubTaskNumber: number;
  TaskID: number;
  TaskTitle: string;
  TypeVariant: null | string;
  VariantID: number;
  VariantName: string;
  YearVariant: null | number;
}

export interface IBlock {
  type: string;
  content: string;
}

=======
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
}

>>>>>>> Stashed changes
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
