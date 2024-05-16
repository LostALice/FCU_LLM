import DefaultLayout from "@/layouts/default";

import { Card, CardHeader, CardBody, CardFooter } from "@nextui-org/card";
import { ScrollShadow } from "@nextui-org/react";
import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/input";

export default function ChatPage() {
  return (
    <DefaultLayout>
      <Card className="flex flex-col items-center justify-center w-full h-[50em] border-1">
        <CardHeader className="border-b-1 justify-between h-[3em]">
          <span>ChatId: asdasd</span>
          <span>機械人可能會出錯。請參考文檔核對重要資訊。</span>
          <span>User: asdasd</span>
        </CardHeader>

        <CardBody className="justify-between">
          <ScrollShadow className="w-full h-full">
            <div className="flex w-full mt-2 space-x-3 max-w-md">
              <div className="p-3 rounded-r-lg rounded-bl-lg bg-blue-600 text-white p-3">
                <p className="text-md">
                  {/* {message} */}
                  \asd
                </p>
              </div>
            </div>
            <div className="flex w-full mt-2 space-x-3 max-w-xs ml-auto justify-end">
              <div>
                <div className="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                  <p className="text-md">
                    askdjguaosdg
                  </p>
                </div>
              </div>
            </div>
          </ScrollShadow>
        </CardBody>

        <CardFooter className="border-t-1 justify-between h-[3em]"></CardFooter>
      </Card>
    </DefaultLayout>
  );
}
