export type cardType = {
  _id?: string; // MongoDBの_idも考慮に入れる場合
  category: string;
  recordNumber: number; // 数値であればnumber型に
  agendaTitle: string;
  content: string;
  proposerName: string;
  file?: string; // 画像ファイル名も考慮に入れる場合
  questionAnswers?: [
    // オプショナルにする場合
    {
      question: string;
      answer: string;
      questioner: string;
    }
  ];
  date?: string; // オプショナルにする場合
};
