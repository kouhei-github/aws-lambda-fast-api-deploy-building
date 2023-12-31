import type { Metadata } from 'next'
import Header from '@/components/Dashboard/Header'

export const metadata: Metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={""}>
      <div>
        <div className={"w-full h-[8vh] bg-blue-400 flex items-center justify-center text-white font-bold"}>header</div>
        <div className={"h-[92vh] flex"}>
          <div className={"h-[92vh] w-[200px] bg-green-500 text-center text-white font-bold"}>sidebar</div>
          <div className={"h-[92vh] flex items-center justify-center w-full bg-gray-200"}>{children}</div>
        </div>
      </div>
      </body>
    </html>
  )
}
