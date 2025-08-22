import React, { useState } from "react";
import "./App.css"; // styles

export default function HostelFaultReportingPortal() {
  const [formData, setFormData] = useState({
    rollNumber: "",
    name: "",
    hostel: "",
    roomNo: "",
    categories: "",
    queries: "",
    image: null,
  });

  const [uploadLabel, setUploadLabel] = useState(
    <>
      <span className="upload-icon">+</span> Upload image(Optional)
    </>
  );

  const [showMenu, setShowMenu] = useState(false); // 👈 toggle for logout menu

  const handleChange = (e) => {
    const { id, value, files } = e.target;
    if (files) {
      setFormData({ ...formData, [id]: files[0] });
      const fileName = files[0]?.name;
      if (fileName) {
        setUploadLabel(
          <>
            <span className="upload-icon" style={{ borderColor: "#28a745" }}>
              ✓
            </span>
            Image: {fileName}
          </>
        );
      }
    } else {
      setFormData({ ...formData, [id]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (
      !formData.rollNumber ||
      !formData.name ||
      !formData.hostel ||
      !formData.roomNo ||
      !formData.categories ||
      !formData.queries
    ) {
      alert(" ❌Please fill in all required fields.");
      return;
    }
    console.log("Feedback submitted:", formData);
    alert("Feedback submitted successfully!");

    setFormData({
      rollNumber: "",
      name: "",
      hostel: "",
      roomNo: "",
      categories: "",
      queries: "",
      image: null,
    });
    setUploadLabel(
      <>
        <span className="upload-icon">+</span> Upload image(Optional)
      </>
    );
  };

  const handleLogout = () => {
    alert("Logged out successfully!");
    // 👉 here you can clear auth tokens, redirect to login page etc.
  };

  return (
    <div>
      <header className="header">
        <div className="logo-section">
          <div className="logo">BIT</div>
        </div>
        <h1 className="title">Hostel Fault Reporting Portal</h1>

        {/* Avatar with dropdown */}
        <div className="avatar-container">
          <button
            className="avatar"
            style={{ color: "white" }}
            onClick={() => setShowMenu(!showMenu)}
          >
            AS
          </button>

          {showMenu && (
            <div className="dropdown-menu">
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </header>

      {/* ==================== FORM ==================== */}
      <div className="form-container">
        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <input
                type="text"
                id="rollNumber"
                placeholder="Roll number"
                value={formData.rollNumber}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="text"
                id="name"
                placeholder="Name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <select
                id="hostel"
                value={formData.hostel}
                onChange={handleChange}
                required
              >
                <option value="">Select your hostel</option>
                <option value="sapphire">Sapphire</option>
                <option value="pearl">Pearl</option>
                <option value="emerald">Emerald</option>
                <option value="diamond">Diamond</option>
                <option value="ruby">Ruby</option>
                <option value="coral">Coral</option>
              </select>
            </div>
            <div className="form-group">
              <input
                type="text"
                id="roomNo"
                placeholder="Room no"
                value={formData.roomNo}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="imageUpload" className="upload-btn">
                {uploadLabel}
              </label>
              <input
                type="file"
                id="imageUpload"
                className="file-input"
                accept="image/*"
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <select
                id="categories"
                value={formData.categories}
                onChange={handleChange}
                required
              >
                <option value="">Select your category</option>
                <option value="electrical">Electrical</option>
                <option value="carpenter">Carpenter</option>
                <option value="restroom">Restroom</option>
                <option value="roomWork">Room Work</option>
                <option value="vending">Vending Machine</option>
                <option value="plumbing">Plumbing</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="form-group" style={{ gridColumn: "1 / -1" }}>
              <textarea
                id="queries"
                className="textarea-large"
                style={{ height: "15rem" }}
                placeholder="Describe your queries..."
                value={formData.queries}
                onChange={handleChange}
                required
              />
            </div>
          </div>
          <button type="submit" className="submit-btn">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}
