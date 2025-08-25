import { useEffect, useState } from "react";
import { IonApp, IonContent } from "@ionic/react";
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

  const fetchNext = async () => {
    const res = await axios.get<Offer>("/offers/next");
    setOffer(res.data);
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
        {offer && (
          <TinderCard onSwipe={onSwipe} preventSwipe={["up", "down"]}>
            <div className="offer-card">
              <h2>{offer.title}</h2>
              <p>{offer.description}</p>
              <p>Expires at: {new Date(offer.expires_at).toLocaleString()}</p>
            </div>
          </TinderCard>
        )}
      </IonContent>
    </IonApp>
  );
}

export default App;
