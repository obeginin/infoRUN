import { lazy, Suspense, useEffect, useRef } from "react";
import { Button } from "../../../ui/buttonDeafault/Button";
import { Input } from "../../../ui/input/Input";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./AdminChangeUser.module.scss";
import { DialogDelete } from "../../../Features/Admin/AdminChangeUser/DialogDelete/DialogDelete";
import { DialogPassword } from "../../../Features/Admin/AdminChangeUser/DialogPassword/DialogPassword";
import { useAdminStore } from "../../../Pages/Admin/store";
import type { ToastMessage } from "primereact/toast";
import { Toast } from "primereact/toast";

const TableUsers = lazy(
  () => import("../../../Features/Admin/AdminChangeUser/TableUsers/TableUsers")
);
import "primereact/resources/themes/lara-light-cyan/theme.css";
import { Spinner } from "../../../ui/LoadingSpinner/LoadingSpinner";

export const AdminChangeUser = () => {
  const toast = useRef<Toast>(null);
  const token = localStorage.getItem("token") || "";
  const { fetchUsers, searchQuery, setSearchQuery, error, success, loading } =
    useAdminStore();

  useEffect(() => {
    fetchUsers(token);
  }, [fetchUsers, token]);

  const showToastMessage = (
    message: string,
    severity: ToastMessage["severity"]
  ) => {
    toast.current?.show({
      severity: severity,
      summary: message,
      life: 3000,
    });
  };

  useEffect(() => {
    if (error) {
      showToastMessage(error, "error");
    }
    if (success) {
      showToastMessage(success, "success");
    }
  }, [error, success]);

  if (loading) {
    return <Spinner />;
  }

  return (
    <>
      <Toast ref={toast} position="bottom-left" />
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
            <Suspense fallback={<Spinner />}>
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