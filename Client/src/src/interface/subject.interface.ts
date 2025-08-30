export interface RootSubject {
  message: string
  count: number
  subjects: Subject[]
}

export interface Subject {
  ID: number
  Name: string
  Description: string
}
