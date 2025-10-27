"use client";

import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { AdminChangeUser } from "@/src/Widgets/Admin/AdminChangeUser/AdminChangeUser";
import { AdminNewUser } from "@/src/Widgets/Admin/AdminNewUser/AdminNewUser";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./admin.module.scss";
import { useAdminStore } from "@/src/store/admin/adminStore";
import { AdminLogsCurrentUser } from "@/src/Widgets/Admin/AdminLogsCurrentUser/AdminLogsCurrentUser";

export default function Admin() {
  const items = [{ id: 1, label: "Панель администратора", link: "/admin" }];
  const { currentUser } = useAdminStore();
  return (
    <>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
        <section>
          <div className={styles.admin__container}>
            <AdminNewUser />
            <AdminChangeUser />

            {currentUser && <AdminLogsCurrentUser />}
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
}
