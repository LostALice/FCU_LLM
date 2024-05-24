// Code by AkinoAlice@TyrantRey

import {
    askQuestionRequestFormat,
    askQuestionResponseFormat,
} from "@/types/api"
import { MessageInfo } from "@/types"

import { siteConfig } from "@/config/site"

export async function askQuestion(
    chatUUID: string,
    question: string,
    userID: string,
    collection: string | "default" = "default"
): Promise<askQuestionResponseFormat> {
    console.log(chatUUID, question, userID, collection)
    const resp = await fetch(siteConfig.api_url + "/chat/" + chatUUID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            chat_id: chatUUID,
            question: question,
            user_id: userID,
            collection: collection,
        }),
    })
    const data = await resp.json()
    return {
        questionUUID: data.question_uuid,
        answer: data.answer,
        fileIDs: data.file_ids,
    }
}
