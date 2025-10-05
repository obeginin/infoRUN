import { IDialog } from "@/src/ui/IDialog/IDialog";
import { useAdminStore } from "@/src/store/adminStore";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { useState, useEffect } from "react";
import { Input } from "@/src/ui/input/Input";
import { Button } from "@/src/ui/buttonDeafault/Button";
export const DialogEdit = () => {
  const { isVisibleDialogEdit, setVisibleDialogEdit, editUser } =
    useAdminStore();
  const currentUser = useAdminStore((state) => state.currentUser);

  const [editedUser, setEditedUser] = useState({
    login: currentUser?.Login || "",
    firstName: currentUser?.First_Name || "",
    lastName: currentUser?.Last_Name || "",
    middleName: currentUser?.Middle_Name || "",
    email: currentUser?.Email || "",
    phone: currentUser?.Phone || "",
    birthDate: currentUser?.BirthDate || "",
    sex: currentUser?.Sex || "",
    roleName: currentUser?.RoleID || 1,
    comment: currentUser?.Comment || "",
    password: "",
    isActive: currentUser?.IsActive || false,
    isDeleted: currentUser?.IsDeleted || false,
  });
  useEffect(() => {
    if (currentUser) {
      setEditedUser({
        login: currentUser.Login,
        lastName: currentUser.Last_Name ? currentUser.Last_Name : "",
        firstName: currentUser.First_Name ? currentUser.First_Name : "",
        middleName: currentUser.Middle_Name ? currentUser.Middle_Name : "",
        email: currentUser.Email,
        phone: currentUser.Phone ? currentUser.Phone : "",
        sex: currentUser.Sex ? currentUser.Sex : "",
        birthDate: currentUser.BirthDate ? currentUser.BirthDate : "",
        comment: currentUser.Comment ? currentUser.Comment : "",
        roleName: currentUser.RoleID,
        isActive: currentUser.IsActive,
        isDeleted: currentUser.IsDeleted,
        password: "",
      });
    }
  }, [currentUser]);

  const handleClick = () => {
    editUser(
      localStorage.getItem("token") || "",
      currentUser?.ID as number,
      editedUser.login,
      editedUser.lastName,
      editedUser.firstName,
      editedUser.middleName,
      editedUser.email,
      editedUser.phone,
      editedUser.sex,
      editedUser.birthDate,
      editedUser.comment,
      editedUser.roleName,
      editedUser.password
    );
  };

  return (
    <IDialog visible={isVisibleDialogEdit} setVdisible={setVisibleDialogEdit}>
      <div>
        <Paragraph size="medium">Изменить пользователя</Paragraph>
        <Input
          label="Логин"
          type="text"
          radius="16px"
          value={editedUser.login}
          onChange={(e) =>
            setEditedUser({ ...editedUser, login: e.target.value })
          }
        />
        <Input
          label="Имя"
          type="text"
          radius="16px"
          value={editedUser.firstName}
          onChange={(e) =>
            setEditedUser({ ...editedUser, firstName: e.target.value })
          }
        />
        <Input
          label="Фамилия"
          type="text"
          radius="16px"
          value={editedUser.lastName}
          onChange={(e) =>
            setEditedUser({ ...editedUser, lastName: e.target.value })
          }
        />
        <Input
          label="Отчество"
          type="text"
          radius="16px"
          value={editedUser.middleName}
          onChange={(e) =>
            setEditedUser({ ...editedUser, middleName: e.target.value })
          }
        />
        <Input
          label="Почта"
          type="text"
          radius="16px"
          value={editedUser.email}
          onChange={(e) =>
            setEditedUser({ ...editedUser, email: e.target.value })
          }
        />
        {/* <Input
          label="Дата рождения"
          type="text"
          radius="16px"
          value={editedUser.birthDate}
          onChange={(e) =>
            setEditedUser({ ...editedUser, birthDate: e.target.value })
          }
        /> */}
        <Input
          label="Пол"
          type="text"
          radius="16px"
          value={editedUser.sex}
          onChange={(e) =>
            setEditedUser({ ...editedUser, sex: e.target.value })
          }
        />
        {/* <Input
          label="Роль"
          type="text"
          radius="16px"
          value={editedUser.roleName}
          onChange={(e) =>
            setEditedUser({ ...editedUser, roleName: e.target.value })
          }
        /> */}
        <Input
          label="Комментарий"
          type="text"
          radius="16px"
          value={editedUser.comment}
          onChange={(e) =>
            setEditedUser({ ...editedUser, comment: e.target.value })
          }
        />
        <Button width="full" outlined onClick={() => handleClick()}>
          Сохранить
        </Button>
      </div>
    </IDialog>
  );
};
