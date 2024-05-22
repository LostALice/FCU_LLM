// Code by AkinoAlice@TyrantRey

export interface askQuestionRequestFormat {
  chatID: string
  question: string
  userID: string | "guest"
  collection: string | "default"
}

export interface askQuestionResponseFormat {
  questionUUID: string
  answer: string
  fileIDs: Array<string>
}