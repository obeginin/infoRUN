"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useUserStore } from "@/src/store/userStore";

export const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const router = useRouter();
  const user = useUserStore((state) => state.user);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token && !user) {
      router.push("/auth");
    } else {
      setIsLoading(false);
    }
  }, [user, router]);

  if (isLoading || !user) {
    return null;
  }

  return children;
};
