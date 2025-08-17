import { useLocation } from "react-router-dom";
import { Footer } from "../../../Widgets/Footer/Footer";
import { Header } from "../../../Widgets/Header/Header";
import { useEffect, useState } from "react";
import type { Task } from "../../../interface/task.interface";
import TasksAPI from "../../../API/tasks";
import { useUserStore } from "../../../store/userStore";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { Spinner } from "../../../ui/LoadingSpinner/LoadingSpinner";
import { Input } from "../../../ui/input/Input";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Paragraph } from "../../../ui/p/Paragraph";
import styles from "./ProfileTask.module.scss";

export const ProfileTask = () => {
  const [data, setData] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState("");

  const location = useLocation();

  const token = localStorage.getItem("token");

  const taskId = Number(location.pathname.split("/")[3]);
  const user = useUserStore((state) => state.user);

  useEffect(() => {
    setLoading(true);
    console.log("Token:", token, "Task ID:", taskId);
    TasksAPI.getTask(user?.ID as number, taskId, token as string)
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, [token, taskId, user?.ID]);

  return (
    <>
      <div className="app">
        <Header />
        <section>
          <ProfileContentContainer>
            {loading ? (
              <div className={styles.spinner__container}>
                <Spinner />
              </div>
            ) : (
              <div>
                {data.length > 0 ? (
                  data.map((item) => (
                    <div key={item.ID} className={styles.task__container}>
                      <div className={styles.task__header}>
                        <div>
                          <Paragraph>{item.Name}</Paragraph>
                          <Paragraph size="tiny" color="gray">
                            {item.VariantName}
                          </Paragraph>
                        </div>
                        <div
                          style={{
                            display: "flex",
                            alignItems: "center",
                            flexDirection: "column",
                          }}
                        ></div>
                      </div>
                      <div className={styles.desctop}>
                        <ProfileContentContainer>
                          <img
                            className={styles.image}
                            src={`${import.meta.env.VITE_BASE_URL}/${
                              item.ImagePath
                            }`}
                          />
                          <div className={styles.response__container}>
                            <Input
                              onChange={(e) => setResponse(e.target.value)}
                              value={response}
                              label="Ответ"
                              required
                              radius="16px"
                            />
                            <Button radius="16px" filled color="white">
                              Отправить
                            </Button>
                          </div>
                        </ProfileContentContainer>
                      </div>
                      <div
                        className={styles.mobile}
                      >
                        <img
                          className={styles.image}
                          src={`${import.meta.env.VITE_BASE_URL}/${
                            item.ImagePath
                          }`}
                        />
                        <div className={styles.response__container}>
                          <Input
                            onChange={(e) => setResponse(e.target.value)}
                            value={response}
                            label="Ответ"
                            required
                            radius="16px"
                          />
                          <Button radius="16px" filled color="white">
                            Отправить
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <p>Нет данных для отображения</p>
                )}
              </div>
            )}
          </ProfileContentContainer>
        </section>
      </div>
      <Footer />
    </>
  );
};
