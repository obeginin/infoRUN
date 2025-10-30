import { Header } from "@/Widgets/Header/Header";
import { Footer } from "@/Widgets/Footer/Footer";
import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import { CurrentMyTask } from "@/Widgets/Constructor/CurrentMyTask/CurrentMyTask";

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
