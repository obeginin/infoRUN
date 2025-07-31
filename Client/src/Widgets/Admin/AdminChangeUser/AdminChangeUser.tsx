import { lazy, Suspense, useEffect } from "react";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Input } from "../../../ui/input/Input";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./AdminChangeUser.module.scss";
import { DialogDelete } from "../../../Features/Admin/AdminChangeUser/DialogDelete/DialogDelete";
import { DialogPassword } from "../../../Features/Admin/AdminChangeUser/DialogPassword/DialogPassword";
import { useAdminStore } from "../../../Pages/Admin/store";
const TableUsers = lazy(
  () => import("../../../Features/Admin/AdminChangeUser/TableUsers/TableUsers")
);

export const AdminChangeUser = () => {
  const token = localStorage.getItem("token") || "";
  const { fetchUsers, searchQuery, setSearchQuery } = useAdminStore();

  useEffect(() => {
    fetchUsers(token);
  }, []);

  return (
    <>
      <ProfileContentContainer>
        <Button disabled filled>
          Назначение ролей
        </Button>
        <Input
          radius="16px"
          type="text"
          label="Поиск по id, email, логину"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <div>
          <div className={styles.user__item}>
            <Suspense fallback={<div>Загрузка........</div>}>
              <TableUsers />
            </Suspense>
          </div>
        </div>
      </ProfileContentContainer>

      <DialogDelete />

      <DialogPassword />
    </>
  );
};

export default AdminChangeUser;
