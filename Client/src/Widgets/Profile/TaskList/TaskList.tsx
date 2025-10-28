// import { Paragraph } from "@/src/ui/p/Paragraph";
// import styles from "./TaskList.module.scss";
// import type { ITask } from "@/src/interface/subtask.interface";
// import { Task } from "@/src/ui/taskContainer/Task";
// import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
// import { Input } from "@/src/ui/input/Input";
// import { Button } from "@/src/ui/buttonDeafault/Button";
// import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
// import { IBlock } from "@/src/interface/subtask.interface";

// interface ITaskList {
//   data: ITask[];
//   isSuccess?: boolean;
//   visibleImage?: number | null;
//   setVisibleImage?: (index: number | null) => void;
//   setAnswer?: (answer: string) => void;
//   handleAnswer?: () => void;
//   isLoading?: boolean;
//   isFetchingMore?: boolean;
//   refetch?: () => void;
//   isError?: boolean;
//   error?: string;
//   limit?: number;
//   answer?: string;
// }

// export const TaskList = ({
//   data,
//   isSuccess=true,
//   visibleImage,
//   setVisibleImage,
//   setAnswer,
//   handleAnswer,
//   isLoading,
//   isFetchingMore,
//   refetch,
//   isError,
//   error,
//   limit = 30,
//   answer,
// }: ITaskList) => {
//   return (
//     <div className={styles.container}>
//       {isSuccess &&
//         data.map((item, index) => (
//           <Task
//             key={index}
//             border={`${
//               item.CompletionStatus === "В процессе"
//                 ? "warning"
//                 : item.CompletionStatus === "Выполнено"
//                 ? "success"
//                 : "primary"
//             }`}
//           >
//             {/* <Paragraph>
//               {item.SubTaskID}: {item.TaskTitle} {item.VariantName}
//             </Paragraph> */}
//             {/* <Paragraph>{item.Score}</Paragraph> */}
//             {/* <i
//               onClick={() =>
//                 setVisibleImage(visibleImage === index ? null : index)
//               }
//               className={`pi pi-angle-down ${styles.arrow}`}
//             ></i> */}
// {/* 
//             <div
//               className={`${styles.collapsible} ${
//                 visibleImage === index ? styles.open : ""
//               }`}
//             > */}
//               <div className={styles.collapsibleInner}>
//                 <ProfileContentContainer>
//                   {item.Blocks.map((block: IBlock, index: number) => (
//                     <div key={index}>
//                       {block.type === "text" && <Paragraph>{block.content}</Paragraph>}
//                       {block.type === "image" && (
//                         <img
//                           src={process.env.NEXT_PUBLIC_BASE_URL + block.content}
//                           alt="image"
//                         />
//                       )}
//                     </div>
//                   ))}
//                   <div className={styles.image}>
//                     <div className={styles.answer}>
//                       {/* <Input
//                         label="Ответ"
//                         value={answer}
//                         onChange={(e) => setAnswer(e.target.value)}
//                         radius="16px"
//                       /> */}
//                       <Button
//                         // onClick={() => handleClick(item.SubTaskID)}
//                         radius="16px"
//                         color="white"
//                         filled
//                       >
//                         Отправить
//                       </Button>
//                     </div>
//                   </div>
//                 </ProfileContentContainer>
//               </div>
//             {/* </div> */}
//           </Task>
//         ))}

//       {isFetchingMore &&
//         Array(limit)
//           .fill(0)
//           .map((_, i) => (
//             <Task key={i}>
//               <Spinner />
//             </Task>
//           ))}
//       {isError && <Paragraph>Произошла ошибка</Paragraph>}
//       {/* <div ref={ref} style={{ height: "1px", visibility: "hidden" }} /> */}
//     </div>
//   );
// };
