import { Header } from "@/src/Widgets/Header/Header";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { CurrentMyTask } from "@/src/Widgets/Constructor/CurrentMyTask/CurrentMyTask";

export default function MyTasks() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Предметы", link: "/profile/subjects" },
  ];
  return (
    <div>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
        <section>
          <ProfileContentContainer>
            <CurrentMyTask />
          </ProfileContentContainer>
        </section>
      </div>
      <Footer />
    </div>
  );
}
