##
## Python version of:
##
## ****************************************************************************
## ALTERNATING BIT AND GO-BACK-N NETWORK SIMULATOR: VERSION 1.1  J.F.Kurose
##
## This code should be used for PA2, unidirectional data-transfer protocols
## from A to B.
## Network properties:
##   - one-way network delay averages 5.0 time units (longer if there
##     are other messages in the channel for GBN), but can be larger
##   - packets can be corrupted (either the header or the data portion)
##     or lost, according to user-defined probabilities
##   - packets will be delivered in the order in which they were sent
##     (although some can be lost).
## 交替位与回退N网络模拟器：版本1.1  J.F.Kurose
##
## 本代码适用于PA2，即从A到B的单向数据传输协议。
## 网络特性：
##   - 单向网络延迟平均为5.0个时间单位（在GBN协议下，若信道中存在其他消息，延迟可能更长），但可能更大
##   - 数据包可能根据用户定义的概率被损坏（无论是头部还是数据部分）或丢失
##   - 数据包将按照发送顺序被传递（尽管部分可能丢失）。
## ****************************************************************************
##
## Python version by:
## Eric Eide <eeide@cs.utah.edu>
## University of Utah
## March 2022
##
## ==> STUDENTS: Implement the methods for EntityA and EntityB.
##
## Run `python3 <thisfile.py> -h` in a terminal window to see the various
## parameters that you can set for a run of this simulator.
##
## This program defines a variable `TRACE` that you can use to conditionally
## print messages from your EntityA and EntityB methods.  For example:
##
##   if TRACE>0:
##       print('A very important event just happened!')
##
## The value of `TRACE` is set by the `-v` command line option.  The default
## value of `TRACE` is 0 (meaning "no tracing").
## ==> 学生：请实现 EntityA 和 EntityB 的方法。
##
## 在终端窗口中运行 `python3 <此文件.py> -h`，查看可以为此模拟器运行设置的各种参数。
##
## 本程序定义了一个变量 `TRACE`，你可以用它来有条件地从 EntityA 和 EntityB 的方法中打印消息。例如：
##
##   if TRACE>0:
##       print('发生了一个非常重要的事件！')
##
## `TRACE` 的值由 `-v` 命令行选项设置。`TRACE` 的默认值为 0（表示“无跟踪”）。
##

import argparse
from copy import deepcopy
from enum import Enum, auto
import random
import sys
import time

###############################################################################

## ************************* BASIC DATA STRUCTURES ****************************
##
## STUDENTS: Do not modify these definitions.
##
## ****************************************************************************

# A Msg is the data unit passed from layer 5 (teacher's code) to layer 4
# (student's code).  It contains the data (bytes) to be delivered to layer 5
# via the student's transport-level protocol entities.
# 消息（Msg）是从第5层（教师代码）传递到第4层（学生代码）的数据单元。  
# 它包含需要通过学生的传输层协议实体传递到第5层的数据（字节）。
#
class Msg:
    MSG_SIZE = 20

    def __init__(self, data):
        self.data = data                # type: bytes[MSG_SIZE]

    def __str__(self):
        return 'Msg(data=%s)' % (self.data)

# A Pkt is the data unit passed from layer 4 (student's code) to layer 3
# (teacher's code).  Note the pre-defined packet structure, which all students
# must follow.
# Pkt（数据包）是从第4层（学生编写的代码）传递到第3层（教师编写的代码）的数据单元。
# 请注意预定义的数据包结构，所有学生都必须遵循此结构。
#
class Pkt:
    def __init__(self, seqnum, acknum, checksum, payload):
        self.seqnum = seqnum            # type: integer
        self.acknum = acknum            # type: integer
        self.checksum = checksum        # type: integer
        self.payload = payload          # type: bytes[Msg.MSG_SIZE]

    def __str__(self):
        return ('Pkt(seqnum=%s, acknum=%s, checksum=%s, payload=%s)'
                % (self.seqnum, self.acknum, self.checksum, self.payload))

###############################################################################

## ***************** STUDENTS WRITE THE NEXT SEVEN METHODS ********************
##
## STUDENTS: When you implement these methods, use instance variables only!
## I.e., variables that you access through `self' like `self.x`.  Do NOT use
## global variables (a.k.a. module-scoped variables) or class variables.
##
## The reason for this restriction is the autograder, which may run several
## simulations within a single Python process.  For each simulation, the
## autograder will create a new instance of EntityA and a new instance of
## EntityB.  If you use global variables and/or class variables in your
## implmentations of EntityA and EntityB, then your code may not work properly
## when run by the autograder, and you may LOSE POINTS!
## 同学们：在实现这些方法时，请仅使用实例变量！ 即，通过 `self` 访问的变量，如 `self.x`。
## 切勿使用全局变量（又称模块作用域变量）或类变量。
##
## 此限制的原因在于自动评分器，它可能会在单个 Python 进程中运行多个
## 模拟。对于每个模拟，自动评分器将创建 EntityA 的新实例和 EntityB 的
## 新实例。如果你在 EntityA 和 EntityB 的实现中使用了全局变量和/或类变量，
## 那么你的代码在自动评分器运行时可能无法正常工作，并可能导致你失分！
##
## If you have any questions about this, please ask the teaching staff.
##
## ****************************************************************************
'''
python -u "./rdtsim_ABP.py" -v 2
'''
import hashlib

def get_checksum(seqnum, acknum, data):
    print('into get_checksum',seqnum, acknum, data)
    checksum = int(hashlib.md5(str(seqnum).encode() + str(acknum).encode() +
                               (data if data else b'')).hexdigest()[:9], 16)
    return checksum

def notcorrupt(packet):
    print('into notcorrupt')
    cou_checksum = get_checksum(packet.seqnum, packet.acknum, packet.payload)
    print(f'cou_checksum == packet.checksum: {cou_checksum, packet.checksum, cou_checksum == packet.checksum}')
    return cou_checksum == packet.checksum

class EntityA:
    # The following method will be called once (only) before any other
    # EntityA methods are called.  You can use it to do any initialization.
    #
    # seqnum_limit is "the number of distinct seqnum values that your protocol
    # may use."  The seqnums and acknums in all layer3 Pkts must be between
    # zero and seqnum_limit-1, inclusive.  E.g., if seqnum_limit is 16, then
    # all seqnums must be in the range 0-15.
    # 以下方法将在调用任何其他EntityA方法之前被调用一次（仅一次）。你可以用它来进行任何初始化操作。
    #
    # seqnum_limit表示“你的协议可以使用的不同序列号值的数量”。
    # 所有layer3 Pkts中的序列号和确认号必须在0到seqnum_limit-1之间，包括这两个值。
    # 例如，如果seqnum_limit为16，那么所有序列号必须在0-15的范围内。
    def __init__(self, seqnum_limit):
        self.sndpkt = None # 保存包的变量
        self.seqnum = 1
        self.acknum = 0
        self.checksum = None
        self.cur_trans = False

    # Called from layer 5, passed the data to be sent to other side.
    # The argument `message` is a Msg containing the data to be sent.
    # 从第5层调用，将待发送的数据传递至另一端。 -> rdt_send(data)
    # 参数 `message` 是一个包含待发送数据的 Msg 对象。
    def output(self, message):
        if self.cur_trans:
            return
        print('='*8)
        print('EntityA output = message: ', message)
        self.cur_trans = True
        self.seqnum = (self.seqnum + 1) % 2 # 序号 0～1
        self.checksum = get_checksum(self.seqnum, self.acknum, message.data)
        self.sndpkt = Pkt(self.seqnum, self.acknum, self.checksum, message.data)
        to_layer3(self, self.sndpkt)
        start_timer(self, 1000)
        print('EntityA output = sndpkt: ', self.sndpkt)

    # Called from layer 3, when a packet arrives for layer 4 at EntityA.
    # The argument `packet` is a Pkt containing the newly arrived packet.
    # 当数据包到达EntityA的第4层时，从第3层调用此函数。 -> rdt_rcv(rcvpkt)
    # 参数`packet`是一个包含新到达数据包的Pkt对象。
    def input(self, packet):
        print('='*8)
        print('into EntityA input = packet', packet)
        if notcorrupt(packet) and (packet.acknum == self.seqnum):
            print('EntityA input - match = packet: ', packet)
            stop_timer(self)
            self.cur_trans = False
        else:
            print('EntityA input - corrupt or not match = packet:', packet)
            print(f'notcorrupt(packet)->{notcorrupt(packet)}')

    # Called when A's timer goes off.
    # 当A的计时器响起时调用。 -> timeout
    def timer_interrupt(self):
        to_layer3(self, self.sndpkt)
        start_timer(self, 1000)

class EntityB:
    # The following method will be called once (only) before any other
    # EntityB methods are called.  You can use it to do any initialization.
    #
    # See comment above `EntityA.__init__` for the meaning of seqnum_limit.
    # 以下方法将在调用任何其他EntityB方法之前被调用一次（仅一次）。你可以使用它进行任何初始化操作。
    #
    # 关于seqnum_limit的含义，请参见`EntityA.__init__`上方的注释。
    def __init__(self, seqnum_limit):
        self.sndpkt = None # 保存包的变量
        self.seqnum = 0
        self.acknum = 0
        self.checksum = None

    # Called from layer 3, when a packet arrives for layer 4 at EntityB.
    # The argument `packet` is a Pkt containing the newly arrived packet.
    # 当第三层接收到一个发往第四层EntityB的数据包时调用此函数。
    # 参数`packet`是一个包含新到达数据包的Pkt对象。
    def input(self, packet):
        print('='*8)
        print('into EntityB input = packet', packet)
        if notcorrupt(packet) and packet.seqnum == self.acknum:
            print('EntityB notcorrupt')
            to_layer5(self, Msg(packet.payload))
            self.checksum = get_checksum(self.seqnum, self.acknum, packet.payload)
            self.sndpkt = Pkt(self.seqnum, self.acknum, self.checksum, packet.payload)
            to_layer3(self, self.sndpkt)
            self.acknum = (self.acknum + 1) % 2 # 序号 0～1
            print('EntityB notcorrupt = sndpkt', self.sndpkt)
        else:
            print('EntityB corrupt')
            to_layer3(self, self.sndpkt)


    # Called when B's timer goes off.
    # 当B的计时器响起时调用。
    def timer_interrupt(self):
        pass

###############################################################################

## ********************** STUDENT-CALLABLE FUNCTIONS **************************
##
## STUDENTS: These are functions that should be called from your EntityA and
## EntityB methods.
##
## The first argument to each of these student-callable functions is the object
## that is invoking the function.  Within an EntityA or EntityB method, that
## object is available as `self`.  For example, to start a timer in one of your
## entity methods, you would do something like:
##
##   start_timer(self, 10.0) # Start a timer that will go off in 10 time units.
##
## Or to send a packet to layer3, you would do something like:
##
##   to_layer3(self, Pkt(...)) # Construct a Pkt and send it to layer3.
## 学生：这些是应从您的EntityA和EntityB方法中调用的函数。
##
## 每个学生可调用函数的第一个参数是调用该函数的对象。
## 在EntityA或EntityB方法中，该对象可作为`self`使用。
## 例如，要在您的实体方法中启动计时器，您可以这样做：
##
##   start_timer(self, 10.0) # 启动一个将在10个时间单位后触发的计时器。
##
## 或者要向layer3发送数据包，您可以这样做：
##
##   to_layer3(self, Pkt(...)) # 构造一个Pkt并将其发送到layer3。
##
## ****************************************************************************

def start_timer(calling_entity, increment):
    the_sim.start_timer(calling_entity, increment)

def stop_timer(calling_entity):
    the_sim.stop_timer(calling_entity)

def to_layer3(calling_entity, packet):
    the_sim.to_layer3(calling_entity, packet)

def to_layer5(calling_entity, message):
    the_sim.to_layer5(calling_entity, message)

def get_time(calling_entity):
    return the_sim.get_time(calling_entity)

###############################################################################

## ****************************************************************************
## ***************** NETWORK SIMULATION CODE STARTS BELOW *********************
##
## The code below simulates the layer 3 and below network environment:
##   - simulates the tranmission and delivery (possibly with bit-level
##     corruption and packet loss) of packets across the layer 3/4 interface
##   - handles the starting/stopping of a timer, and generates timer
##     interrupts (resulting in calling student's timer handler).
##   - generates message to be sent (passed from later 5 to 4)
##
## THERE IS NO REASON THAT ANY STUDENT SHOULD HAVE TO READ OR UNDERSTAND
## THE CODE BELOW.  YOU SHOULD NOT TOUCH OR REFERENCE (in your code) ANY
## OF THE DATA STRUCTURES BELOW.  If you're interested in how I designed
## the simulator, you're welcome to look at the code - but again, you should
## not have to, and you definitely should not have to modify.
## 以下代码模拟了第三层及以下的网络环境：
##   - 模拟数据包在第三层/第四层接口之间的传输和交付（可能包含比特级
##     损坏和丢包）
##   - 处理计时器的启动/停止，并生成计时器中断（导致调用学生的计时器处理程序）
##   - 生成要发送的消息（从第五层传递到第四层）
##
## 没有任何理由要求学生必须阅读或理解以下代码。  
## 你不应触碰或引用（在你的代码中）以下任何数据结构。  
## 如果你对我如何设计模拟器感兴趣，欢迎查看代码——但再次强调，你不必这样做，也绝对不需要修改它。
##
## ****************************************************************************

class EventType(Enum):
    TIMER_INTERRUPT = auto()
    FROM_LAYER5 = auto()
    FROM_LAYER3 = auto()

class Event:
    def __init__(self, ev_time, ev_type, ev_entity, packet=None):
        self.ev_time = ev_time      # float
        self.ev_type = ev_type      # EventType
        self.ev_entity = ev_entity  # EntityA or EntityB
        self.packet = packet        # Pkt or None

class Simulator:
    def __init__(self, options, cbA=None, cbB=None):
        self.n_sim                = 0
        self.n_sim_max            = options.num_msgs
        self.time                 = 0.000
        self.interarrival_time    = options.interarrival_time
        self.loss_prob            = options.loss_prob
        self.corrupt_prob         = options.corrupt_prob
        self.seqnum_limit         = options.seqnum_limit
        self.n_to_layer3_A        = 0
        self.n_to_layer3_B        = 0
        self.n_lost               = 0
        self.n_corrupt            = 0
        self.n_to_layer5_A        = 0
        self.n_to_layer5_B        = 0

        if options.random_seed is None:
            self.random_seed      = time.time_ns()
        else:
            self.random_seed      = options.random_seed
        random.seed(self.random_seed)

        if self.seqnum_limit < 2:
            self.seqnum_limit_n_bits = 0
        else:
            # How many bits to represent integers in [0, seqnum_limit-1]?
            self.seqnum_limit_n_bits = (self.seqnum_limit-1).bit_length()

        self.trace                = options.trace
        self.to_layer5_callback_A = cbA
        self.to_layer5_callback_B = cbB

        self.entity_A             = EntityA(self.seqnum_limit)
        self.entity_B             = EntityB(self.seqnum_limit)
        self.event_list           = []

    def get_stats(self):
        stats = {'n_sim'             : self.n_sim,
                 'n_sim_max'         : self.n_sim_max,
                 'time'              : self.time,
                 'interarrival_time' : self.interarrival_time,
                 'loss_prob'         : self.loss_prob,
                 'corrupt_prob'      : self.corrupt_prob,
                 'seqnum_limit'      : self.seqnum_limit,
                 'random_seed'       : self.random_seed,
                 'n_to_layer3_A'     : self.n_to_layer3_A,
                 'n_to_layer3_B'     : self.n_to_layer3_B,
                 'n_lost'            : self.n_lost,
                 'n_corrupt'         : self.n_corrupt,
                 'n_to_layer5_A'     : self.n_to_layer5_A,
                 'n_to_layer5_B'     : self.n_to_layer5_B
        }
        return stats

    def run(self):
        if self.trace>0:
            print('\n===== SIMULATION BEGINS')

        self._generate_next_arrival()

        while (self.event_list
               and self.n_sim < self.n_sim_max):
            ev = self.event_list.pop(0)
            if self.trace>2:
                print(f'\nEVENT time: {ev.ev_time}, ', end='')
                if ev.ev_type == EventType.TIMER_INTERRUPT:
                    print(f'timer_interrupt, ', end='')
                elif ev.ev_type == EventType.FROM_LAYER5:
                    print(f'from_layer5, ', end='')
                elif ev.ev_type == EventType.FROM_LAYER3:
                    print(f'from_layer3, ', end='')
                else:
                    print(f'unknown_type, ', end='')
                print(f'entity: {ev.ev_entity}')

            self.time = ev.ev_time

            if ev.ev_type == EventType.FROM_LAYER5:
                self._generate_next_arrival()
                j = self.n_sim % 26
                m = bytes([97+j for i in range(Msg.MSG_SIZE)])
                if self.trace>2:
                    print(f'          MAINLOOP: data given to student: {m}')
                self.n_sim += 1
                ev.ev_entity.output(Msg(m))

            elif ev.ev_type == EventType.FROM_LAYER3:
                ev.ev_entity.input(deepcopy(ev.packet))

            elif ev.ev_type == EventType.TIMER_INTERRUPT:
                ev.ev_entity.timer_interrupt()

            else:
                print('INTERNAL ERROR: unknown event type; event ignored.')

        if self.trace>0:
            print('===== SIMULATION ENDS')

    def _insert_event(self, event):
        if self.trace>2:
            print(f'            INSERTEVENT: time is {self.time}')
            print(f'            INSERTEVENT: future time will be {event.ev_time}')
        # Python 3.10+: use the bisect module:
        # insort(self.event_list, event, key=lambda e: e.ev_time)
        i = 0
        while (i < len(self.event_list)
               and self.event_list[i].ev_time < event.ev_time):
            i += 1
        self.event_list.insert(i, event)

    def _generate_next_arrival(self):
        if self.trace>2:
            print('          GENERATE NEXT ARRIVAL: creating new arrival')

        x = self.interarrival_time * 2.0 * random.random()
        ev = Event(self.time+x, EventType.FROM_LAYER5, self.entity_A)
        self._insert_event(ev)

    #####

    def _valid_entity(self, e, method_name):
        if (e is self.entity_A
            or e is self.entity_B):
            return True
        print(f'''WARNING: entity in call to `{method_name}` is invalid!
  Invalid entity: {e}
  Call ignored.''')
        return False

    def _valid_increment(self, i, method_name):
        if ((type(i) is int or type(i) is float)
            and i >= 0.0):
            return True
        print(f'''WARNING: increment in call to `{method_name}` is invalid!
  Invalid increment: {i}
  Call ignored.''')
        return False

    def _valid_message(self, m, method_name):
        if (type(m) is Msg
            and type(m.data) is bytes
            and len(m.data) == Msg.MSG_SIZE):
            return True
        print(f'''WARNING: message in call to `{method_name}` is invalid!
  Invalid message: {m}
  Call ignored.''')
        return False

    def _valid_packet(self, p, method_name):
        if (type(p) is Pkt
            and type(p.seqnum) is int
            and 0 <= p.seqnum < self.seqnum_limit
            and type(p.acknum) is int
            and 0 <= p.acknum < self.seqnum_limit
            and type(p.checksum) is int
            and type(p.payload) is bytes
            and len(p.payload) == Msg.MSG_SIZE):
            return True
        # Issue special warnings for invalid seqnums and acknums.
        if (type(p.seqnum) is int
            and not (0 <= p.seqnum < self.seqnum_limit)):
            print(f'''WARNING: seqnum in call to `{method_name}` is invalid!
  Invalid packet: {p}
  Call ignored.''')
        elif (type(p.acknum) is int
              and not (0 <= p.acknum < self.seqnum_limit)):
            print(f'''WARNING: acknum in call to `{method_name}` is invalid!
  Invalid packet: {p}
  Call ignored.''')
        else:
            print(f'''WARNING: packet in call to `{method_name}` is invalid!
  Invalid packet: {p}
  Call ignored.''')
        return False

    #####

    def start_timer(self, entity, increment):
        if not self._valid_entity(entity, 'start_timer'):
            return
        if not self._valid_increment(increment, 'start_timer'):
            return

        if self.trace>2:
            print(f'          START TIMER: starting timer at {self.time}')

        for e in self.event_list:
            if (e.ev_type == EventType.TIMER_INTERRUPT
                and e.ev_entity is entity):
                print('WARNING: attempt to start a timer that is already started!')
                return

        ev = Event(self.time+increment, EventType.TIMER_INTERRUPT, entity)
        self._insert_event(ev)

    def stop_timer(self, entity):
        if not self._valid_entity(entity, 'stop_timer'):
            return

        if self.trace>2:
            print(f'          STOP TIMER: stopping timer at {self.time}')

        i = 0
        while i < len(self.event_list):
            if (self.event_list[i].ev_type == EventType.TIMER_INTERRUPT
                and self.event_list[i].ev_entity is entity):
                break
            i += 1
        if i < len(self.event_list):
            self.event_list.pop(i)
        else:
            print('WARNING: unable to stop timer; it was not running.')

    def to_layer3(self, entity, packet):
        if not self._valid_entity(entity, 'to_layer3'):
            return
        if not self._valid_packet(packet, 'to_layer3'):
            return

        if entity is self.entity_A:
            receiver = self.entity_B
            self.n_to_layer3_A += 1
        else:
            receiver = self.entity_A
            self.n_to_layer3_B += 1

        # Simulate losses.
        if random.random() < self.loss_prob:
            self.n_lost += 1
            if self.trace>0:
                print('          TO_LAYER3: packet being lost')
            return

        seqnum = packet.seqnum
        acknum = packet.acknum
        checksum = packet.checksum
        payload = packet.payload

        # Simulate corruption.
        if random.random() < self.corrupt_prob:
            self.n_corrupt += 1
            x = random.random()
            if (x < 0.75
                or self.seqnum_limit_n_bits == 0):
                payload = b'Z' + payload[1:]
            elif x < 0.875:
                # Flip a random bit in the seqnum.
                # The result might be greater than seqnum_limit if seqnum_limit
                # is not a power of two.  This is OK.
                # Recall that randrange(x) returns an int in [0, x).
                seqnum ^= 2**random.randrange(self.seqnum_limit_n_bits)
                # Kurose's simulator simply did:
                # seqnum = 999999
            else:
                # Flip a random bit in the acknum.
                acknum ^= 2**random.randrange(self.seqnum_limit_n_bits)
                # Kurose's simulator simply did:
                # acknum = 999999
            if self.trace>0:
                print('          TO_LAYER3: packet being corrupted')

        # Compute the arrival time of packet at the other end.
        # Medium cannot reorder, so make sure packet arrives between 1 and 9
        # time units after the latest arrival time of packets
        # currently in the medium on their way to the destination.
        last_time = self.time
        for e in self.event_list:
            if (e.ev_type == EventType.FROM_LAYER3
                and e.ev_entity is receiver):
                last_time = e.ev_time
        arrival_time = last_time + 1.0 + 8.0*random.random()

        p = Pkt(seqnum, acknum, checksum, payload)
        ev = Event(arrival_time, EventType.FROM_LAYER3, receiver, p)
        if self.trace>2:
            print('          TO_LAYER3: scheduling arrival on other side')
        self._insert_event(ev)

    def to_layer5(self, entity, message):
        if not self._valid_entity(entity, 'to_layer5'):
            return
        if not self._valid_message(message, 'to_layer5'):
            return

        if entity is self.entity_A:
            self.n_to_layer5_A += 1
            callback = self.to_layer5_callback_A
        else:
            self.n_to_layer5_B += 1
            callback = self.to_layer5_callback_B

        if self.trace>2:
            print(f'          TO_LAYER5: data received: {message.data}')
        if callback:
            callback(message.data)

    def get_time(self, entity):
        if not self._valid_entity(entity, 'get_time'):
            return
        return self.time

###############################################################################

TRACE = 0

the_sim = None

def report_config():
    stats = the_sim.get_stats()
    print(f'''SIMULATION CONFIGURATION
--------------------------------------
(-n) # layer5 msgs to be provided:      {stats['n_sim_max']}
(-d) avg layer5 msg interarrival time:  {stats['interarrival_time']}
(-z) transport protocol seqnum limit:   {stats['seqnum_limit']}
(-l) layer3 packet loss prob:           {stats['loss_prob']}
(-c) layer3 packet corruption prob:     {stats['corrupt_prob']}
(-s) simulation random seed:            {stats['random_seed']}
--------------------------------------''')

def report_results():
    stats = the_sim.get_stats()
    time = stats['time']
    if time > 0.0:
        tput = stats['n_to_layer5_B']/time
    else:
        tput = 0.0
    print(f'''\nSIMULATION SUMMARY
--------------------------------
# layer5 msgs provided to A:      {stats['n_sim']}
# elapsed time units:             {stats['time']}

# layer3 packets sent by A:       {stats['n_to_layer3_A']}
# layer3 packets sent by B:       {stats['n_to_layer3_B']}
# layer3 packets lost:            {stats['n_lost']}
# layer3 packets corrupted:       {stats['n_corrupt']}
# layer5 msgs delivered by A:     {stats['n_to_layer5_A']}
# layer5 msgs delivered by B:     {stats['n_to_layer5_B']}
# layer5 msgs by B/elapsed time:  {tput}
--------------------------------''')

def main(options, cb_A=None, cb_B=None):
    global TRACE
    TRACE = options.trace

    global the_sim
    the_sim = Simulator(options, cb_A, cb_B)
    report_config()
    the_sim.run()

#####

if __name__ == '__main__':
    desc = 'Run a simulation of a reliable data transport protocol.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', type=int, default=10,
                        dest='num_msgs',
                        help=('number of messages to simulate'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-d', type=float, default=100.0,
                        dest='interarrival_time',
                        help=('average time between messages'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-z', type=int, default=16,
                        dest='seqnum_limit',
                        help=('seqnum limit for data transport protocol; '
                              'all packet seqnums must be >=0 and <limit'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-l', type=float, default=0.0,
                        dest='loss_prob',
                        help=('packet loss probability'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-c', type=float, default=0.0,
                        dest='corrupt_prob',
                        help=('packet corruption probability'
                              ' [float, default: %(default)s]'))
    parser.add_argument('-s', type=int,
                        dest='random_seed',
                        help=('seed for random number generator'
                              ' [int, default: %(default)s]'))
    parser.add_argument('-v', type=int, default=0,
                        dest='trace',
                        help=('level of event tracing'
                              ' [int, default: %(default)s]'))
    options = parser.parse_args()

    main(options)
    report_results()
    sys.exit(0)

###############################################################################

## End of program.
