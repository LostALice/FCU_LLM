import { title } from "@/components/primitives"
import DefaultLayout from "@/layouts/default"

export default function DocsPage() {
  return (
    <DefaultLayout>
      <section className="flex flex-col items-center justify-center">
        <div className="inline-block text-center justify-center">
          <h1 className={title()}>逢甲大學課程問答機械人</h1>
        </div>
      </section>
      <section className="flex flex-col items-center justify-center p-5">
        <div className="inline-block text-center justify-center">
          <h2>
            歡迎來到逢甲大學課程問答機械人的專屬頁面！
          </h2>
          <h2>
            在這裡，您可以即時獲得有關課程的所有問題的答案。不論是關於課程表、學分還是其他任何問題。
          </h2>
        </div>
      </section>
    </DefaultLayout>
  )
}
