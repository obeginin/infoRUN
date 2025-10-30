"use client";

import TasksAPI from "@/API/tasks";
import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import { ITask } from "@/interface/subtask.interface";
import { Paragraph } from "@/ui/p/Paragraph";
import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import { format } from "date-fns";
import { useSearchParams } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import { useIntersectionObserver } from "@siberiacancode/reactuse";
import { Spinner } from "@/ui/LoadingSpinner/LoadingSpinner";
import { Task } from "@/ui/taskContainer/Task";
import styles from "./selectedTask.module.scss";
import { Nullable } from "primereact/ts-helpers";
import { FiltersForm } from "@/Widgets/CatalogSelectedTask/FiltersForm";
import { ITaskSelected } from "@/Widgets/CatalogSelectedTask/Tasks";

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
    async (
      currentOffset: number,
      filters?: { creator: string; date: Nullable<Date>; id: Nullable<number> }
    ) => {
      if (!subject || !task) return;

      setIsFetchingMore(true);
      try {
        const filterCreator = filters?.creator || creator;
        const filterDate = filters?.date || date;
        const filterId = filters?.id || id;

        const response = await TasksAPI.getSelectedTask(
          Number(subject),
          Number(task),
          token,
          limit,
          currentOffset,
          filterCreator,
          format(filterDate as Date, "yyyy-MM-dd") as string,
          Number(filterId)
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
    [subject, task, token, limit]
  );

  const handleApplyFilters = () => {
    setOffset(0);
    setData([]);
    fetchTasks(0, { creator, date, id });
  };

  // Первоначальная загрузка данных
  useEffect(() => {
    setOffset(0);
    setData([]);
    fetchTasks(0);
  }, [fetchTasks]);

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
            <FiltersForm
              handleApplyFilters={handleApplyFilters}
              creator={creator}
              setCreator={setCreator}
              date={date}
              setDate={setDate}
              id={id}
              setId={setId}
            />

            <Paragraph>Найдено задач: {data.length}</Paragraph>

            <ProfileContentContainer>
              <div className={styles.container}>
                <ITaskSelected
                  data={data}
                  visibleImages={visibleImages}
                  handleOpenBlocks={handleOpenBlocks}
                />

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
