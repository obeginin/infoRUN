"use client";

import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import { AdminChangeUser } from "@/Widgets/Admin/AdminChangeUser/AdminChangeUser";
import { AdminNewUser } from "@/Widgets/Admin/AdminNewUser/AdminNewUser";
import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import styles from "./admin.module.scss";
import { useAdminStore } from "@/store/admin/adminStore";
import { AdminLogsCurrentUser } from "@/Widgets/Admin/AdminLogsCurrentUser/AdminLogsCurrentUser";

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
