import { useEffect, useState } from "react";
import { IonApp, IonContent, IonText } from "@ionic/react";
import TinderCard from "react-tinder-card";
import axios from "axios";

interface Offer {
  id: number;
  title: string;
  description: string;
  referral_link?: string;
  promo_code?: string;
  expires_at: string;
}

function App() {
  const [offer, setOffer] = useState<Offer | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const fetchNext = async () => {
    try {
      const res = await axios.get<Offer>("/offers/next");
      if (res.data) {
        setOffer(res.data);
        setMessage(null);
      } else {
        setOffer(null);
        setMessage("No offers available");
      }
    } catch (err) {
      setOffer(null);
      if (axios.isAxiosError(err)) {
        const detail = err.response?.data as { detail?: string };
        setMessage(detail?.detail || err.message);
      } else {
        setMessage("Failed to fetch offer");
      }
    }
  };

  useEffect(() => {
    fetchNext();
  }, []);

  const onSwipe = async (dir: string) => {
    if (!offer) return;
    if (dir === "right") {
      await axios.post(`/offers/${offer.id}/like`, { user_id: 1 });
    }
    fetchNext();
  };

  return (
    <IonApp>
      <IonContent fullscreen>
        {offer ? (
          <TinderCard onSwipe={onSwipe} preventSwipe={["up", "down"]}>
            <div className="offer-card">
              <h2>{offer.title}</h2>
              <p>{offer.description}</p>
              <p>Expires at: {new Date(offer.expires_at).toLocaleString()}</p>
            </div>
          </TinderCard>
        ) : (
          message && (
            <IonText color="medium">
              <p>{message}</p>
            </IonText>
          )
        )}
      </IonContent>
    </IonApp>
  );
}

export default App;
