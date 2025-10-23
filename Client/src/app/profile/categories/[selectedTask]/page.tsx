"use client";

import TasksAPI from "@/src/API/tasks";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { IBlock, ITask } from "@/src/interface/subtask.interface";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { format } from "date-fns";
import { useSearchParams } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import { useIntersectionObserver } from "@siberiacancode/reactuse";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import { Task } from "@/src/ui/taskContainer/Task";
import styles from "./selectedTask.module.scss";
import { Input } from "@/src/ui/input/Input";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Nullable } from "primereact/ts-helpers";
import { MyCalendar } from "@/src/ui/calendar/Calendar";

export default function SelectedTask() {
  const searchParams = useSearchParams();
  const subject = searchParams.get("subject");
  const task = searchParams.get("task");
  const [data, setData] = useState<ITask[]>([]);
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const [visibleImages, setVisibleImages] = useState<number[]>([]);
  const token = localStorage.getItem("token") || "";

  const [creator, setCreator] = useState("");
  const [date, setDate] = useState<Nullable<Date>>(null);
  const [id, setId] = useState<Nullable<number>>(null);
  const limit = 10;

  const fetchTasks = useCallback(
    async (currentOffset: number) => {
      if (!subject || !task) return;

      setIsFetchingMore(true);
      try {
        const response = await TasksAPI.getSelectedTask(
          Number(subject),
          Number(task),
          token,
          limit,
          currentOffset,
          creator,
          format(date as Date, "yyyy-MM-dd") as string,
          Number(id)
        );

        const newData = response.data || response;
        setData((prev) =>
          currentOffset === 0 ? newData : [...prev, ...newData]
        );
        setHasMore(newData.length === limit);
      } catch (err) {
        console.log(err);
      } finally {
        setIsFetchingMore(false);
      }
    },
    [subject, task, token, limit, creator, date, id]
  );

  useEffect(() => {
    setOffset(0);
    setData([]);
    fetchTasks(0);
  }, [fetchTasks, creator, date, id]);

  const { ref } = useIntersectionObserver<HTMLDivElement>({
    threshold: 1,
    onChange: (entry) => {
      if (entry.isIntersecting && hasMore && !isFetchingMore) {
        const newOffset = offset + limit;
        setOffset(newOffset);
        fetchTasks(newOffset);
      }
    },
  });

  const handleOpenBlocks = (index: number) => {
    if (visibleImages.includes(index)) {
      setVisibleImages((prev) => prev.filter((i) => i !== index));
    } else {
      setVisibleImages((prev) => [...prev, index]);
    }
  };

  return (
    <>
      <Header />
      <div className="app">
        <section>
          <div>
            <div className={styles.filters}>
              <Input
                value={creator}
                onChange={(e) => setCreator(e.target.value)}
                label="Поиск по автору"
              />
              <Input
                value={String(id)}
                onChange={(e) => setId(Number(e.target.value))}
                label="Поиск по ID"
                type="number"
              />
              <MyCalendar
                value={date}
                onChange={(e) => setDate(e.value)}
                showIcon
                dateFormat="dd.mm.yy"
              />

              <Button onClick={() => fetchTasks(0)} filled color="white">
                Применить фильтры
              </Button>
            </div>

            <ProfileContentContainer>
              <div className={styles.container}>
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
                                format(
                                  new Date(item.CreatedDate),
                                  "dd.MM.yyyy"
                                )}
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
                          item.Blocks.map(
                            (block: IBlock, blockIndex: number) => (
                              <div key={blockIndex}>
                                {block.type === "text" && (
                                  <p>{block.content}</p>
                                )}
                                {block.type === "image" && (
                                  <img
                                    src={
                                      process.env.NEXT_PUBLIC_BASE_URL +
                                      block.content
                                    }
                                    alt="image"
                                  />
                                )}
                              </div>
                            )
                          )}
                      </ProfileContentContainer>
                    </div>
                  ))}

                {isFetchingMore &&
                  Array(limit)
                    .fill(0)
                    .map((_, i) => (
                      <Task key={i}>
                        <Spinner />
                      </Task>
                    ))}
                {/* {isError && <Paragraph>Произошла ошибка</Paragraph>} */}
                <div
                  ref={ref}
                  style={{ height: "1px", visibility: "hidden" }}
                />
              </div>
            </ProfileContentContainer>
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
}
