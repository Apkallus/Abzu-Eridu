#include <stdio.h>
#include <string.h>

struct rtpkt {
  int sourceid;       /* id of sending router sending this pkt */
  int destid;         /* id of router to which pkt being sent 
                         (must be an immediate neighbor) */
  int mincost[4];    /* min cost to node 0 ... 3 */
};

extern int TRACE;
extern int YES;
extern int NO;

struct distance_table 
{
  int costs[4][4];
} dt0;


/* students to write the following two routines, and maybe some others */
// rtinit0() 
// 这个例程将在模拟开始时被调用一次。rtinit0()没有参数。
// 它应该将节点 0 中的距离表（见下文）初始化为反映到节点 1、2 和 3 的直接成本分别为 1、3 和 7。在上面的图中，
// 所有链路都是双向的，并且两个方向的成本相同。初始化距离表后，以及任何其他你的节点 0 例程所需的数据结构，
// 它应该将其直接连接的邻居（在这种情况下是 1、2 和 3）发送给所有其他网络节点的最小成本路径的成本，
// 即它的距离向量。这些最小成本信息通过调用下面描述的例程 tolayer2()，以路由数据包的形式发送给相邻节点。
// 路由数据包的格式也在下面描述。
void rtinit0() 
{
  dt0.costs[0][0] = 0;
  dt0.costs[0][1] = 1;
  dt0.costs[0][2] = 3;
  dt0.costs[0][3] = 7;

  for(int row = 0; row <= 3; row++){
    if(row == 0){
      continue;
    }
    for(int col = 0; col <= 3; col++){
      dt0.costs[row][col] = 999;
    }
  }

  printdt0(dt0);

  struct rtpkt to1, to2, to3;
  to1.sourceid = 0;
  to1.destid = 1;
  memcpy(to1.mincost, dt0.costs[0], 4*sizeof(int));

  memcpy(to2.mincost, to1.mincost, 4*sizeof(struct rtpkt));
  memcpy(to3.mincost, to1.mincost, 4*sizeof(struct rtpkt));
  to2.destid = 2;
  to3.destid = 3;

  tolayer2(to1);
  tolayer2(to2);
  tolayer2(to3);
}

// rtupdate0(struct rtpkt *rcvdpkt). 
// 这个例程将在节点 0 接收到由其一个直接连接的邻居发送给它的路由数据包时被调用。
// 参数 *rcvdpkt 是接收到的数据包的指针。
void rtupdate0(rcvdpkt)
  struct rtpkt *rcvdpkt;
{

}


printdt0(dtptr)
  struct distance_table *dtptr;
  
{
  printf("                via     \n");
  printf("   D0 |    1     2    3 \n");
  printf("  ----|-----------------\n");
  printf("     1|  %3d   %3d   %3d\n",dtptr->costs[1][1],
	 dtptr->costs[1][2],dtptr->costs[1][3]);
  printf("dest 2|  %3d   %3d   %3d\n",dtptr->costs[2][1],
	 dtptr->costs[2][2],dtptr->costs[2][3]);
  printf("     3|  %3d   %3d   %3d\n",dtptr->costs[3][1],
	 dtptr->costs[3][2],dtptr->costs[3][3]);
}

linkhandler0(linkid, newcost)   
  int linkid, newcost;

/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
/* 当从0到linkid的成本从当前值变为newcost时调用 */
/* 如果你是本科生，可以留空此例程。如果你想 */
/* 使用此例程，你需要将prog3.c中的LINKCHANGE */
/* 常量定义从0改为1 */

{
}

