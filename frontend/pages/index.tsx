import { title } from "@/components/primitives";
import DefaultLayout from "@/layouts/default";

import { Card, CardHeader, CardBody } from "@nextui-org/card";

export default function MainPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center">
        <div className="inline-block text-center justify-center">
          <h1 className={title()}>逢甲大學課程問答機械人</h1>
        </div>
      </section>
      <section className="flex flex-col items-center justify-center p-8">
        <div className="inline-block text-center justify-center">
          <h2>歡迎來到逢甲大學課程問答機械人的專屬頁面！</h2>
          <h2>
            在這裡，您可以即時獲得有關課程的所有問題的答案。不論是關於課程表、學分還是其他任何問題。
          </h2>
        </div>
      </section>
      <section className="items-center justify-center p-8">
        <div className="flex flex-wrap gap-8 h-[50vh]">
          <Card isPressable shadow="md" className="flex-1 w-1/4 rounded-xl">
            <CardHeader className="items-center">
              <span className="bold text-3xl text-center bg-transparent">
                文檔
              </span>
            </CardHeader>
            <CardBody className="content-center overflow-visible p-0 hover:scale-110 hover:transform duration-300">
              asd
            </CardBody>
          </Card>

          <Card isPressable shadow="md" className="flex-1 w-1/4 rounded-xl">
            <CardHeader className="items-center">
              <span className="bold text-3xl text-center bg-transparent">
                文檔
              </span>
            </CardHeader>
            <CardBody className="content-center overflow-visible p-0 hover:scale-110 hover:transform duration-300">
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
              <h3 className="text-center">asdlajsdb</h3>
            </CardBody>
          </Card>
        </div>
      </section>
    </DefaultLayout>
  );
}
