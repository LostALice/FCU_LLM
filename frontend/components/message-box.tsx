"use client"

import { FC } from "react";
import { Divider } from "@nextui-org/divider";
import { Tooltip } from "@nextui-org/tooltip";
import { Button } from "@nextui-org/button";
import { Link } from "@nextui-org/link";

export interface messageInfo {
	message?: string;
	attachments?: Array<string>;
	time?: string;
}

export const MessageBox: FC<messageInfo> = ({ message, attachments, time }) => {
	return (
		<Tooltip
			content={time}
			placement="bottom-end"
			delay={5}
			offset={-29}
		>
			<div className="border rounded-lg odd:border-green-500 border-emerald-600 m-3">
				<div className="justify-around p-4">
					<span className="">{message}</span>
					<Divider className="my-2" />
					<div className="flex justify-between">
						<div className="">
							{attachments?.map((attachment: string) => (
								<Button
									size="sm"
									isExternal
									href={"./docs/" + attachment}
									key={attachment}
									as={Link}
									showAnchorIcon
									className="mr-1 text-medium"
								>
									{attachment}
								</Button>
							))}
						</div>
						{/* <span className="">{time}</span> */}
					</div>
				</div>
			</div>
		</Tooltip>
	);
};
