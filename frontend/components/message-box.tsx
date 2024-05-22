"use client"

import { FC } from "react";
import { Divider } from "@nextui-org/divider";
import { Tooltip } from "@nextui-org/tooltip";
import { Button } from "@nextui-org/button";
import { Link } from "@nextui-org/link";

import { MessageInfo } from "@/types";


// export function MessageBox({ questionUUID, question, answer, attachments, time }): FC<MessageInfo> {
export const MessageBox: FC<MessageInfo> = ({ questionUUID, question, answer, attachments, time }) => {
	return (
		<Tooltip
			content={<span>{time}  {questionUUID}</span>}
			placement="bottom-end"
			delay={5}
			offset={-29}
		>
			<div className="border rounded-lg border-emerald-600 m-3">
				<div className="justify-around p-4">
					<span className="italic">{question}</span>
					<Divider className="my-2" />
					<span className="">{answer}</span>
					<Divider className="my-2" />
					<div className="flex justify-between">
						<div className="text-left">
							{attachments?.map((attachment) => (
								<Tooltip
									content={<span className="text-left">{attachment}</span>}
									placement="bottom"
									key={attachment}
								>
									<Button
										size="sm"
										isExternal
										href={"./docs/" + attachment}
										key={attachment}
										as={Link}
										showAnchorIcon
										className="mr-3 text-small w-[7rem] animate-marquee1 whitespace-nowrap"
									>
										<span className="text-left truncate italic">{attachment}</span>
									</Button>
								</Tooltip>
							))}
						</div>
					</div>
				</div>
			</div>
		</Tooltip >
	);
};
