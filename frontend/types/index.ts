import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export interface MessageInfo {
  chatUUID: string;
  questionUUID: string;
  question: string;
  answer: string;
  time: string;
  attachments: Array<string>;
}
