import Head from 'next/head';
import styles from '../styles/Home.module.css';
import Link from 'next/link';

export default function Home() {
  return (
    <div>
      <h1>
        <Link href={'/schedule'}>test</Link>
      </h1>
    </div>
  );
}
