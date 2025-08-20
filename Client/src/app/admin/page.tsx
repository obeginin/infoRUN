import { BreadCrumb } from "@/src/Features/BreadCrumb/BreadCrumb";
import { AdminChangeUser } from "@/src/Widgets/Admin/AdminChangeUser/AdminChangeUser";
import { AdminNewUser } from "@/src/Widgets/Admin/AdminNewUser/AdminNewUser";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import styles from "./admin.module.scss"

export default function Admin() {
  return (
    <>
      <div className="app">
        <Header />
        <BreadCrumb currentPage="Панель администратора" />
        <section>
          <div className={styles.admin__container}>
            <AdminNewUser />
            <AdminChangeUser />
          </div>
        </section>
      </div>
      <Footer />
    </>
  );
}
