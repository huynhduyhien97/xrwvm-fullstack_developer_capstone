const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const cors = require("cors");

const Reviews = require("./review");
const Dealerships = require("./dealership");

const app = express();
const port = 3030;

app.use(cors());
app.use(express.json());


const reviewsData = JSON.parse(
  fs.readFileSync("reviews.json", "utf8")
);

const dealershipsData = JSON.parse(
  fs.readFileSync("dealerships.json", "utf8")
);


mongoose.connect(
  "mongodb://mongo_db:27017/dealershipsDB"
);


mongoose.connection.once(
  "open",
  async () => {
    console.log("MongoDB connected");

    await Reviews.deleteMany({});
    await Dealerships.deleteMany({});

    await Reviews.insertMany(
      reviewsData.reviews
    );

    await Dealerships.insertMany(
      dealershipsData.dealerships
    );

    console.log("Initial data loaded");
  }
);


app.get("/", (req, res) => {
  res.send(
    "Welcome to the Dealership API"
  );
});


app.get(
  "/fetchReviews",
  async (req, res) => {
    try {
      const reviews = await Reviews.find();

      res.json(reviews);
    } catch (error) {
      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.get(
  "/fetchReviews/dealer/:id",
  async (req, res) => {
    try {
      const reviews = await Reviews.find({
        dealership: Number(req.params.id),
      });

      res.json(reviews);
    } catch (error) {
      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.get(
  "/fetchDealers",
  async (req, res) => {
    try {
      const dealers =
        await Dealerships.find();

      res.json(dealers);
    } catch (error) {
      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.get(
  "/fetchDealers/:state",
  async (req, res) => {
    try {
      const dealers =
        await Dealerships.find({
          state: req.params.state,
        });

      res.json(dealers);
    } catch (error) {
      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.get(
  "/fetchDealer/:id",
  async (req, res) => {
    try {
      const dealer =
        await Dealerships.find({
          id: Number(req.params.id),
        });

      res.json(dealer);
    } catch (error) {
      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.post(
  "/insert_review",
  async (req, res) => {
    try {
      const data = req.body;

      const lastReview = await Reviews
        .findOne()
        .sort({ id: -1 });

      const newId = lastReview
        ? lastReview.id + 1
        : 1;

      const review = new Reviews({
        id: newId,
        name: data.name,
        dealership: Number(
          data.dealership
        ),
        review: data.review,
        purchase: data.purchase,
        purchase_date:
          data.purchase_date,
        car_make: data.car_make,
        car_model: data.car_model,
        car_year: Number(
          data.car_year
        ),
      });

      const savedReview =
        await review.save();

      res.json(savedReview);

    } catch (error) {
      console.error(error);

      res.status(500).json({
        error: error.message,
      });
    }
  }
);


app.listen(
  port,
  () => {
    console.log(
      `Server is running on http://localhost:${port}`
    );
  }
);