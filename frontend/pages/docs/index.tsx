import DefaultLayout from "@/layouts/default";
import { useState, useEffect} from "react";

import { DepartmentList } from "@/types";

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
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [department, setDepartment] = useState<string[]>([]);
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

  useEffect(() => {
    async () => {
      setDepartment([...department]);
    };
  }, []);

  // const departmentList = department.map(item => {
  //   <ListboxItem className="truncate" key={item}>
  //     {item}
  //   </ListboxItem>;
  // })

  return (
    <DefaultLayout>
      <div className="flex">
        <ScrollShadow className="w-[10rem]" size={30}>
          <Listbox
            aria-label="Actions"
            className="h-full "
            onAction={(key) => console.log(key)}
            variant="flat"
            selectionMode="single"
            emptyContent={<Spinner color="success" label="加載中..." />}
          >
            <ListboxItem key="new">new file</ListboxItem>
          </Listbox>
        </ScrollShadow>

        <Table aria-label="file table">
          <TableHeader>
            <TableColumn key="name">文件名稱</TableColumn>
            <TableColumn key="height">最後更新日期</TableColumn>
          </TableHeader>
          <TableBody
            items={list.items}
            isLoading={isLoading}
            loadingContent={<Spinner color="success" label="加載中..." />}
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
