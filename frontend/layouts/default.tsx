import { Navbar } from "@/components/navbar";
import { Link } from "@nextui-org/link";
import { Head } from "./head";

import Transition from "@/components/transition";

export default function DefaultLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<div className="relative flex flex-col h-screen">
			<Head />
			<Navbar />
			<main className="container mx-auto max-w-7xl px-6 flex-grow pt-16">
				<Transition>
					{children}
				</Transition>
			</main>
			<footer className="w-full flex items-center justify-center py-3">
				<Link
					isExternal
					className="flex items-center gap-1 text-current"
					href="https://github.com/LostALice"
					title="Do you know the magic?"
				>
					<span className="italic">Copyright © Aki.no.Alice@TyrantRey 張紹謙 2022-2026</span>
				</Link>
			</footer>
		</div>
	);
}
