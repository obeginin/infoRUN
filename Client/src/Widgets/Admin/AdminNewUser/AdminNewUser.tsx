"use client";

import { Button } from "../../../ui/buttonDeafault/Button";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import { useEffect, useState, useCallback } from "react";
import AdminAPI from "../../../API/admin";
import { Input } from "../../../ui/input/Input";
import styles from "./AdminNewUser.module.scss";
import { useAdminStore } from "@/store/admin/adminStore";
import { TextContainer } from "@/ui/textContainer/TextContainer";

interface IData {
  RoleID: number;
  Name: string;
}

export const AdminNewUser = () => {
  const [formData, setFormData] = useState({
    user: "",
    telephone: "",
    email: "",
    password: "",
    name: "",
    surname: "",
  });

  const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
  const [sex, setSex] = useState<"М" | "Ж">("М");
  const [data, setData] = useState<IData[]>([]);

  const [errors, setErrors] = useState({
    user: "",
    email: "",
    password: "",
    role: "",
  });

  const [touched, setTouched] = useState({
    user: false,
    email: false,
    password: false,
  });

  const token = localStorage.getItem("token");
  const addNewUser = useAdminStore((state) => state.addNewUser);

  useEffect(() => {
    AdminAPI.adminRoles(token ? token : "")
      .then((response) => setData(response))
      .catch((error) => console.log(error));
  }, [token]);

  // Валидация отдельных полей
  const validateField = useCallback((name: string, value: string) => {
    switch (name) {
      case "user":
        if (!value.trim()) return "Логин обязателен";
        if (/[А-Яа-яЁё]/.test(value))
          return "Логин должен содержать только латинские буквы";
        if (value.length < 3) return "Логин должен быть не менее 3 символов";
        return "";

      case "password":
        if (!value) return "Пароль обязателен";
        if (value.length < 6) return "Пароль должен быть не менее 6 символов";
        return "";

      case "email":
        if (!value) return "Email обязателен";
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))
          return "Введите корректный email";
        return "";

      default:
        return "";
    }
  }, []);

  const validateForm = useCallback(() => {
    const newErrors = {
      user: validateField("user", formData.user),
      email: validateField("email", formData.email),
      password: validateField("password", formData.password),
      role: !selectedRoleId ? "Выберите роль" : "",
    };

    setErrors(newErrors);
    return !Object.values(newErrors).some((error) => error !== "");
  }, [formData, selectedRoleId, sex, validateField]);

  const handleFieldChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));

    // Валидация при изменении (только для touched полей)
    if (touched[field as keyof typeof touched]) {
      setErrors((prev) => ({
        ...prev,
        [field]: validateField(field, value),
      }));
    }
  };

  const handleBlur = (field: string) => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    setErrors((prev) => ({
      ...prev,
      [field]: validateField(field, formData[field as keyof typeof formData]),
    }));
  };

  const handleClick = () => {
    // Помечаем все поля как touched для показа всех ошибок
    const newTouched = {
      user: true,
      email: true,
      password: true,
    };
    setTouched(newTouched);

    // Валидируем все поля
    const newErrors = {
      user: validateField("user", formData.user),
      email: validateField("email", formData.email),
      password: validateField("password", formData.password),
      role: !selectedRoleId ? "Выберите роль" : "",
    };

    setErrors(newErrors);

    // Проверяем есть ли ошибки
    const hasErrors = Object.values(newErrors).some((error) => error !== "");
    if (hasErrors) {
      return;
    }

    addNewUser(
      token ? token : "",
      formData.user,
      formData.surname,
      formData.name,
      formData.email,
      formData.telephone,
      sex,
      selectedRoleId ? selectedRoleId : 1,
      formData.password
    );
  };

  // Убрали вызов validateForm() из тела компонента

  return (
    <>
      <ProfileContentContainer>
        <div className={styles.container}>
          <TextContainer >
            Новый пользователь
          </TextContainer>
          <div className={styles.form}>
            <Input
              radius="16px"
              value={formData.user}
              onChange={(e) => handleFieldChange("user", e.target.value)}
              type="text"
              label="Логин *"
              error_text={errors.user}
            />

            <Input
              radius="16px"
              value={formData.name}
              onChange={(e) => handleFieldChange("name", e.target.value)}
              type="text"
              label="Имя"
            />

            <Input
              radius="16px"
              value={formData.surname}
              onChange={(e) => handleFieldChange("surname", e.target.value)}
              label="Фамилия"
            />

            <Input
              radius="16px"
              value={formData.telephone}
              type="tel"
              onChange={(e) => handleFieldChange("telephone", e.target.value)}
              label="Телефон"
            />

            <Input
              radius="16px"
              value={formData.email}
              onChange={(e) => handleFieldChange("email", e.target.value)}
              type="email"
              label="Email *"
              error_text={errors.email}
            />

            <Input
              radius="16px"
              value={formData.password}
              onChange={(e) => handleFieldChange("password", e.target.value)}
              type="password"
              label="Пароль *"
              error_text={errors.password}
            />

            <div className={styles.select__container}>
              <i className={`pi pi-chevron-down ${styles.icon}`} />
              <select
                className={styles.select}
                value={sex}
                onChange={(e) => setSex(e.target.value as "М" | "Ж")}
              >
                <option value="">Выберите пол *</option>
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
                <option value="">Выберите роль *</option>
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
              {errors.role && (
                <span className={styles.error}>{errors.role}</span>
              )}
          </div>

          <Button filled color="white" outlined onClick={handleClick}>
            Сохранить
          </Button>
        </div>
      </ProfileContentContainer>
    </>
  );
};
