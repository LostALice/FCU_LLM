import { useState, useEffect } from 'react'

import { MessageBox } from "@/components/message-box"
import DefaultLayout from "@/layouts/default"
import { siteConfig } from "@/config/site"

import { Card, CardHeader, CardBody } from "@nextui-org/card";
import { ScrollShadow } from "@nextui-org/react";
import { Tooltip } from "@nextui-org/tooltip";
import { Textarea } from "@nextui-org/input";
import { Button } from "@nextui-org/button";

interface messageInfo {
  messageID: number;
  messageContent: string;
  attachments: Array<string>;
  time: string;
}

export default function ChatPage() {
  const [inputQuestion, setInputQuestion] = useState("");
  const [chatMessage, setChatMessage] = useState<messageInfo[]>([]);
  const [chatUUID, setChatUUID] = useState<string>("");
  const [isLoading, setLoading] = useState(true)

  function sendMessage(event: React.MouseEvent<HTMLButtonElement>) {
    if (inputQuestion == "") {
      return
    }

    const message: messageInfo = {
      messageID: Math.floor(Math.random() * 100),
      messageContent: inputQuestion,
      attachments: ["asd", "dsa"],
      time: new Date().toDateString()
    }

    setChatMessage([...chatMessage, message])
    setInputQuestion("")
  }

  useEffect(() => {
    setLoading(true)
    fetch(siteConfig.api_url + "/uuid")
      .then((res) => res.json())
      .then((data) => {
        setChatUUID(data)
        setLoading(false)
      })
  }, [])

  return (
    <DefaultLayout>
      <Card className="flex flex-col items-center justify-center w-full h-[50rem] border-1">
        <CardHeader className="grid grid-cols-1 border-b-1 h-[3em] overflow-hidden lg:grid-cols-3">
          <span className="text-start hidden lg:block">{chatUUID}</span>
          <span className="text-center text-small">機械人可能會出錯。請參考文檔核對重要資訊。</span>
          <span className="text-end hidden lg:block">使用者: 未登入</span>
        </CardHeader>
        <CardBody className="justify-between">
          <ScrollShadow className="w-full h-full items-center">
            {chatMessage.map((item) => (
              <MessageBox
                key={item.messageID}
                message={item.messageContent}
                attachments={item.attachments}
                time={item.time}
              />
            ))}
          </ScrollShadow>
        </CardBody>
        <div className="flex justify-between w-[90%] h-[3rem] mb-2">
          <Textarea
            name="question"
            className="h-[2rem] w-full"
            placeholder="開始提問"
            value={inputQuestion}
            onValueChange={setInputQuestion}
            disabled={isLoading ? true : false}
          />
          <Button
            disabled={chatMessage ? false : true}
            onClick={sendMessage}>
            送出
          </Button>
        </div>
      </Card>
    </DefaultLayout>
  );
}
