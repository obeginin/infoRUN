'use client'

import { Button } from "../../../ui/buttonDeafault/Button";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { useEffect, useState } from "react";
import AdminAPI from "../../../API/admin";
import { Input } from "../../../ui/input/Input";
import styles from "./AdminNewUser.module.scss";
import { useAdminStore } from "@/src/store/adminStore";
interface IData {
  RoleID: number;
  Name: string;
}
export const AdminNewUser = () => {
  const [user, setUser] = useState<string>("");
  const [telephone, setTelephone] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
  const [sex, setSex] = useState<"М" | "Ж">("М");
  const [name, setName] = useState<string>("");
  const [surname, setSurname] = useState<string>("");

  const token = localStorage.getItem("token");
  const [data, setData] = useState<IData[]>([]);

  const [loginError, setLoginError] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [phoneError, setPhoneError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  const addNewUser = useAdminStore((state) => state.addNewUser);

  useEffect(() => {
    AdminAPI.adminRoles(token ? token : "")
      .then((response) => setData(response))
      .catch((error) => console.log(error));
  }, [token]);

  const handleClick = () => {
    if (/[А-Яа-яЁё]/.test(user)) {
      setLoginError(true);
      return;
    }
    if (/[0-9]/.test(telephone) && telephone.length < 10) {
      setPhoneError(true);
      return;
    }
    if (!email.includes("@") && email.includes(".")) {
      setEmailError(true);
      return;
    }
    if (password.length <= 6) {
      setPasswordError(true);
      return;
    }

    addNewUser(
      token ? token : "",
      user,
      surname,
      name,
      email,
      telephone,
      sex,
      selectedRoleId ? selectedRoleId : 1,
      password
    );
  };

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
          <Button outlined onClick={() => handleClick()}>
            Сохранить
          </Button>
        </div>
        <div className={styles.form}>
          <Input
            radius="16px"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            type="text"
            label="Имя пользователя"
            error_text={
              loginError ? "Логин должен состоять только из букв" : ""
            }
          />
          <Input
            radius="16px"
            value={name}
            onChange={(e) => setName(e.target.value)}
            type="text"
            label="Имя"
          />
          <Input
            radius="16px"
            value={surname}
            onChange={(e) => setSurname(e.target.value)}
            label="Фамилия"
          />
          <Input
            radius="16px"
            value={telephone}
            type="text"
            onChange={(e) => setTelephone(e.target.value)}
            label="Телефон"
            error_text={phoneError ? "Введите корректный номер" : ""}
          />
          <Input
            radius="16px"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="text"
            label="Email"
            error_text={emailError ? "Введите корректную почту" : ""}
          />
          <Input
            radius="16px"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="text"
            label="Пароль"
            error_text={
              passwordError ? "Пароль должен быть больше 6 символов" : ""
            }
          />
          <div className={styles.select__container}>
            <i className={`pi pi-chevron-down ${styles.icon}`} />
            <select
              className={styles.select}
              value={sex}
              onChange={(e) => setSex(e.target.value as "М" | "Ж")}
            >
              <option value="М" className={styles.option}>
                Мужской
              </option>
              <option value="Ж" className={styles.option}>
                Женский
              </option>
            </select>
          </div>
          <div className={styles.select__container}>
            <i className={`pi pi-chevron-down ${styles.icon}`} />
            <select
              className={styles.select}
              value={selectedRoleId || ""}
              onChange={(e) => setSelectedRoleId(+e.target.value || null)}
            >
              {data?.map((item: IData) => (
                <option
                  key={item.RoleID}
                  value={item.RoleID}
                  className={styles.option}
                >
                  {item.Name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </ProfileContentContainer>
    </>
  );
};
