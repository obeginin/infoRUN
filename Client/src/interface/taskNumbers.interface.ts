export interface RootTask {
  message: string
  count: number
  tasks: Task[]
}

export interface Task {
  TaskID: number
  TaskNumber: number
  TaskTitle: string
  SubjectID: number
}
