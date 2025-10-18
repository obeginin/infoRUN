"use client";

import TasksAPI from "@/src/API/tasks";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { IBlock, ITask } from "@/src/interface/subtask.interface";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
export default function SelectedTask() {
  const searchParams = useSearchParams();
  const subject = searchParams.get("subject");
  const task = searchParams.get("task");
  const [data, setData] = useState<ITask[]>([]);
  const token = localStorage.getItem("token") || "";

  useEffect(() => {
    TasksAPI.getSelectedTask(Number(subject), Number(task), token)
      .then((res) => setData(res.data))
      .catch((err) => console.log(err));
  }, [subject, task, token]);

  return (
    <>
      <Header />
      <div className="app">
        <section>
          <div>
            {data.length > 0 ? (
              data.map((item: ITask) => (
                <div key={item.TaskID}>
                  <ProfileContentContainer>
                    <h2>{item.Creator}</h2>
                    <p>{item.TaskTitle}</p>

                    {item.Blocks.map((block: IBlock, index: number) => (
                      <div key={index}>
                        {block.type === "text" && <p>{block.content}</p>}
                        {block.type === "image" && (
                          <img
                            src={
                              process.env.NEXT_PUBLIC_BASE_URL + block.content
                            }
                            alt="image"
                          />
                        )}
                      </div>
                    ))}
                  </ProfileContentContainer>
                </div>
              ))
            ) : (
              <Paragraph>Задание не найдено</Paragraph>
            )}
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
}
