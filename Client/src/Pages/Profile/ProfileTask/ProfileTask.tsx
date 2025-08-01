import { useLocation } from "react-router-dom";
import { Footer } from "../../../Widgets/Footer/Footer";
import { Header } from "../../../Widgets/Header/Header";
import { useEffect, useState } from "react";
import type { Task } from "../../../interface/task.interface";
import TasksAPI from "../../../API/tasks";
import { useUserStore } from "../../../store/userStore";

export const ProfileTask = () => {
  const [data, setData] = useState<Task[]>([]);
  const location = useLocation();
  const token = localStorage.getItem("token");

  const user = useUserStore((state) => state.user);
  const taskId = Number(location.pathname.split("/")[3]);

  useEffect(() => {
    console.log("Token:", token, "Task ID:", taskId);
    TasksAPI.getTask(user?.ID as number , taskId, token as string)
      .then((res) => {
        setData(res);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, [token, taskId]);

  return (
    <div className="app">
      <Header />
      <main>
        {data.length > 0 ? (
          data.map((item) => (
            <div key={item.ID}>
              <h2>{item.Name}</h2>
              <p>{item.VariantName}</p>
              <p>{item.ImagePath}</p>
            </div>
          ))
        ) : (
          <p>Нет данных для отображения</p>
        )}
      </main>
      <Footer />
    </div>
  );
};
