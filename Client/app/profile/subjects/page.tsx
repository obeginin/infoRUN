import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import { SubjectList } from "@/Features/SubjectsList/SubjectList";
export default function Subjects() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Предметы", link: "/profile/subjects" },
  ];
  return (
    <div style={{ position: "relative", minHeight: "100vh" }}>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
        <section>
          <ProfileContentContainer>
            <SubjectList to="/profile/subjects" />
          </ProfileContentContainer>
        </section>
      </div>
      <Footer />
    </div>
  );
}
