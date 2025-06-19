"""Simple Instagram scraper using instaloader.

This module replaces the old Selenium based scraper and relies on the
``instaloader`` library which internally interacts with the official
Instagram endpoints. It is more resilient to website layout changes.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional
import json
import instaloader


@dataclass
class PostData:
    url: str
    caption: Optional[str]
    hashtags: List[str]
    mentions: List[str]
    timestamp: str
    likes: int
    comments_count: int


@dataclass
class ProfileData:
    username: str
    full_name: str
    biography: str
    followers: int
    following: int
    posts_count: int
    posts: List[PostData]


class InstaloaderScraper:
    """Scraper powered by instaloader."""

    def __init__(self, login: str | None = None, password: str | None = None) -> None:
        self.loader = instaloader.Instaloader()
        if login and password:
            self.loader.login(login, password)

    def fetch_profile(self, username: str) -> ProfileData:
        profile = instaloader.Profile.from_username(self.loader.context, username)
        posts: List[PostData] = []
        for p in profile.get_posts():
            posts.append(
                PostData(
                    url=f"https://www.instagram.com/p/{p.shortcode}/",
                    caption=p.caption,
                    hashtags=list(p.caption_hashtags),
                    mentions=list(p.caption_mentions),
                    timestamp=p.date_utc.isoformat(),
                    likes=p.likes,
                    comments_count=p.comments,
                )
            )
        return ProfileData(
            username=profile.username,
            full_name=profile.full_name,
            biography=profile.biography,
            followers=profile.followers,
            following=profile.followees,
            posts_count=profile.mediacount,
            posts=posts,
        )

    def save_as_json(self, profile: ProfileData, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(asdict(profile), fh, ensure_ascii=False, indent=2)


def main() -> None:
    username = input("Enter profile username: ").strip()
    scraper = InstaloaderScraper()
    data = scraper.fetch_profile(username)
    scraper.save_as_json(data, f"{username}_data.json")
    print(f"Saved profile data to {username}_data.json")


if __name__ == "__main__":
    main()
