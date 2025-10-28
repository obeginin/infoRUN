import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { IBlock, ITask } from "@/src/interface/subtask.interface";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { format } from "date-fns";
import styles from "./Tasks.module.scss";
interface ITaskSelected {
  data: ITask[];
  visibleImages: number[];
  handleOpenBlocks: (index: number) => void;
}

export const ITaskSelected = ({
  data,
  visibleImages,
  handleOpenBlocks,
}: ITaskSelected) => {
  return (
    <>
      {Array.isArray(data) &&
        data.map((item: ITask, index: number) => (
          <div key={`${item.SubTaskID}-${index}`}>
            <ProfileContentContainer>
              <div className={styles.header_wrapper}>
                <div
                  style={{
                    display: "flex",
                    gap: "20px",
                  }}
                >
                  <Paragraph>
                    {item.SubTaskID}: {item.TaskTitle}
                  </Paragraph>
                  <Paragraph italic color="gray">
                    {item.CreatedDate &&
                      format(new Date(item.CreatedDate), "dd.MM.yyyy")}
                  </Paragraph>
                  <Paragraph>{item.Creator}</Paragraph>
                </div>
                <i
                  className={`pi pi-angle-down`}
                  style={{
                    transform: visibleImages.includes(index)
                      ? "rotate(180deg)"
                      : "rotate(0deg)",
                    transition: "transform 0.3s ease-in-out",
                  }}
                  onClick={() => handleOpenBlocks(index)}
                />
              </div>

              {visibleImages.includes(index) &&
                item.Blocks &&
                Array.isArray(item.Blocks) &&
                item.Blocks.map((block: IBlock, blockIndex: number) => (
                  <div key={blockIndex}>
                    {block.type === "text" && <p>{block.content}</p>}
                    {block.type === "image" && (
                      <img
                        src={process.env.NEXT_PUBLIC_BASE_URL + block.content}
                        alt="image"
                      />
                    )}
                  </div>
                ))}
            </ProfileContentContainer>
          </div>
        ))}
    </>
  );
};
