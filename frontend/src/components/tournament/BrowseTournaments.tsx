import axios from "axios"
import React, { useEffect, useState } from "react"

interface Tournament {
  obj_id: Number,
  name: String,
  time_start: String,
  time_end: String,
  time_finish: String,
  max_number_of_participants: String,
  discipline_id: Number,
  organizer_id: Number,
  sponsor_id: Number
}

interface PaginatedResults<T> {
  items: T[];
  page: number;
  total_pages: number;
  total_results: number;
}

const getTournaments = async (page: number, pageSize: number, pattern: String): Promise<PaginatedResults<Tournament>> => {
  const response = await axios.get(`http://localhost:8000/api/v1/tournament?name=${pattern}&page=${page}`)
  const data = await response.data;

  return data;
}

const BrowseTournaments = () => {

  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [pattern, setPattern] = useState("");
  const [inPattern, setInPattern] = useState("");

  useEffect(() => {
    const fetchTournaments = async () => {
      const paginatedResults = await getTournaments(page, pageSize, pattern);
      setTournaments(paginatedResults.items);
    }

    fetchTournaments();
  }, [page, pageSize, pattern]);

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const handleNextPage = () => {
    if (tournaments.length > 0) {
      setPage(page + 1);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInPattern(e.target.value);
  }

  const handleNewPattern = () => {
    setPattern(inPattern);
  }

  return <>
    <div>
      <input className="form-control" type="text" onChange={handleChange} />
      <button className="btn btn-primary" onClick={handleNewPattern}>Search</button>
    </div>

    <button className="btn btn-primary" onClick={handlePreviousPage}>Previous</button>
    <span> - {page} - </span>
    <button className="btn btn-primary" onClick={handleNextPage}>Next</button>
    {tournaments.length === 0 && (
      <p>Empty</p>
    )}
    {tournaments.map((item) => (
      <div className="row">
        <div className="col-md-6">
          <h2>{item.name}</h2>
        </div>
      </div>
    ))}
  </>
}

export default BrowseTournaments;
