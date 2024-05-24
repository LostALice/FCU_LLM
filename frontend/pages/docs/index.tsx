import DefaultLayout from "@/layouts/default";
import { useState } from "react";

import { Listbox, ListboxItem } from "@nextui-org/listbox";
import { ScrollShadow } from "@nextui-org/scroll-shadow";
import { Spinner } from "@nextui-org/spinner";
import {
  Table,
  TableHeader,
  TableBody,
  TableColumn,
  TableRow,
  TableCell,
} from "@nextui-org/table";

export default function DocsPage() {
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const [fileList, setFileList] = useState<string[]>([]);

  const list = {
    items: [
      {
        name: "asd",
        name2: "asd",
      },
      {
        name: "das",
        name2: "ASd",
      },
    ],
  };

  return (
    <DefaultLayout>
      {/* <section className="flex flex-col items-center justify-center gap-4">
        <div className="inline-block max-w-lg text-center justify-center">
          <h1 className={title()}>文檔</h1>
        </div>
      </section> */}

      <div className="flex h-[50rem]">
        <ScrollShadow className="w-[15rem]" size={30}>
          <Listbox
            aria-label="Actions"
            className="h-full"
            onAction={(key) => console.log(key)}
            variant="flat"
            selectionMode="single"
          >
            <ListboxItem key="new">New file</ListboxItem>
            <ListboxItem key="copy">Copy link</ListboxItem>
            <ListboxItem key="edit">Edit file</ListboxItem>
            <ListboxItem key="delete">Delete file</ListboxItem>
          </Listbox>
        </ScrollShadow>

        <Table aria-label="file table">
          <TableHeader>
            <TableColumn key="name">Name</TableColumn>
            <TableColumn key="height">Height</TableColumn>
          </TableHeader>
          <TableBody
            items={list.items}
            isLoading={isLoading}
            loadingContent={<Spinner label="Loading..." />}
          >
            {(item) => (
              <TableRow key={item.name}>
                <TableCell> {item.name} </TableCell>
                <TableCell> {item.name2} </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </DefaultLayout>
  );
}
