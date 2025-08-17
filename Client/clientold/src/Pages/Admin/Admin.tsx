import { BreadCrumb } from "../../Features/BreadCrumb/BreadCrumb";
import { Footer } from "../../Widgets/Footer/Footer";
import { Header } from "../../Widgets/Header/Header";
import styles from "./Admin.module.scss";
import { AdminNewUser } from "../../Widgets/Admin/AdminNewUser/AdminNewUser";
import { AdminChangeUser } from "../../Widgets/Admin/AdminChangeUser/AdminChangeUser";
export const Admin = () => {
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
};
