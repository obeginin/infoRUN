import { Li, Ul } from "../../ui/ul-li/UlLi";

interface ListHeaderProps {
  children: React.ReactNode[];
}

export const ListHeader = ({
  children,
}: ListHeaderProps) => {
  return (
    <>
      <Ul

      >
        {children.map((item, index) => (
          <Li key={index}>{item}</Li>
        ))}
      </Ul>
    </>
  );
};
