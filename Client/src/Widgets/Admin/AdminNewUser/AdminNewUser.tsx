import { Button } from "../../../ui/buttonDeafault/Button";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { useEffect, useState } from "react";
import AdminAPI from "../../../API/admin";
import { Input } from "../../../ui/input/Input";
import styles from "./AdminNewUser.module.scss"

interface IData {
  RoleID: number;
  Name: string
}

export const AdminNewUser = () => {
  const [user, setUser] = useState<string>("");
  const [telephone, setTelephone] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const token = localStorage.getItem("token");
  const [data, setData] = useState<IData[]>([]);
  useEffect(() => {
    AdminAPI.adminRoles(token ? token : "")
      .then((response) => setData(response))
      .catch((error) => console.log(error));
  }, [token]);
  
  return (
    <>
      <ProfileContentContainer>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            gap: "10px",
          }}
        >
          <Button disabled filled color="white">
            Новый пользователь
          </Button>
          <Button outlined>Сохранить</Button>
        </div>
        <Input
          radius="16px"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          type="text"
          label="Имя пользователя"
        />
        <Input
          radius="16px"
          value={telephone}
          onChange={(e) => setTelephone(e.target.value)}
          type="text"
          label="Телефон"
        />
        <Input
          radius="16px"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="text"
          label="Email"
        />
        <Input
          radius="16px"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="text"
          label="Пароль"
        />
        <select className={styles.select}>
          {data.map((item, index) => (
            <option key={index} value={item.Name} className={styles.option}>
              {item.Name}
            </option>
          ))}
        </select>
      </ProfileContentContainer>
    </>
  );
};
